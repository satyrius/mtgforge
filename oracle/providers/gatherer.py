import re
import urllib
from lxml import etree
from urlparse import urlparse, urlunparse

from oracle.models import PageState
from oracle.providers import (
    HomePage, ProviderPage, ProviderCardListPage, ProviderCardPage,
    map_result_as_pages, cache_parsed
)


def gettext(elem):
    parts = [elem.text or '']
    for e in elem:
        parts.append(gettext(e))
        if e.tail:
            parts.append(e.tail)
    return ' '.join(parts).strip()


def normalized_text(text):
    nl = '__new_line__'
    text = re.sub(u'\n', nl, text)
    text = re.sub(u'\xa0', ' ', text)
    text = re.sub(u'\xe2\x80\x99|\u2019', '\'', text)
    text = re.sub(u'\s*(\xe2\x80\x94|\u2014)\s*', ' - ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    text = re.sub(r'(?<!\(|\{|\s)\{', ' {', text)
    text = re.sub(r'\}(?!=\)|\}|\s|\:)', '} ', text)
    text = re.sub(r'}\s+{', '}{', text)
    text = re.sub(u'{0}\s*'.format(nl), '\n', text)
    return text.strip()


def normalized_element_text(elem):
    text = gettext(elem)
    return normalized_text(text)


class GathererPage(ProviderPage):
    provider_name = 'gatherer'

    def set_parsed(self):
        self.change_state(PageState.PARSED)

    def is_parsed(self):
        return self.state == PageState.PARSED


class GathererHomePage(HomePage, GathererPage):
    def products_list_generator(self):
        select_id = 'ctl00_ctl00_MainContent_Content_SearchControls_setAddText'
        for o in self.doc.cssselect('select#{0} option'.format(select_id)):
            name = o.get('value')
            if not name:
                continue
            query = u'/Pages/Search/Default.aspx?' + urllib.quote_plus(u'set=["{0}"]'.format(name), '=')
            yield name, self.absolute_url(query), None


class CardNotFound(Exception):
    pass


class ParseError(Exception):
    pass


class GathererCard(ProviderCardPage, GathererPage):
    def _encode_mana(self, html_el):
        mana_re = re.compile(r'name=(.+?)&')
        for img in html_el.cssselect('img'):
            mana = unicode(mana_re.search(img.get('src')).groups()[0])
            img.tail = u'{' + mana + u'}' + unicode(img.tail or '')
        etree.strip_elements(html_el, 'img', with_tail=False)

    def parse_mana(self, html_el):
        self._encode_mana(html_el)
        return normalized_element_text(html_el)

    def parse_text(self, html_el):
        blocks = []
        for block in html_el.cssselect('div.cardtextbox'):
            self._encode_mana(block)
            blocks.append(normalized_element_text(block))
        return '\n'.join(blocks)

    def parse_flavor(self, html_el):
        return self.parse_text(html_el)

    def parse_rarity(self, html_el):
        value = normalized_element_text(html_el)
        # Workaround with Wizards' dummies
        if value == u'Basic Land':
            value = u'Common'
        return value

    @cache_parsed()
    def details(self, forward=True):
        """Return card face details from current page. Matches given card name
        with the found one.

        Keyword argumets:
        forward -- navigate to related pages for additional info
        """
        if not self.name:
            raise Exception('Cannot get details for page with unknown name')

        faces = self.doc.cssselect('table.cardDetails')
        if not faces:
            raise ParseError('No one card face found on this page')

        parts = {}
        # Workaround with multipart (splited) cards. Splited card page content
        # is not relevant to requested card name, so we have to navigate to
        # url with 'part' get parameter. Parse navigation block (Oracle/Printed
        # switcher) to find link to the correct page.
        if len(faces) == 1:
            navi = faces[0].cssselect(
                '#ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rightCol '
                'div.smallGreyMono')[0]
            if re.search(r'This is one part of the multi-part card',
                         gettext(navi)):
                for a in navi.cssselect('ul li a'):
                    m = re.match(u'[^(]+\(([^)]+)\)', gettext(a))
                    if m:
                        parts[m.group(1)] = a.get('href')

        found = False
        name_row_key = 'name'
        subcontent_re = re.compile('MainContent_SubContent_SubContent')
        mvid_re = re.compile('multiverseid\=(?P<id>\d+)')
        for face in faces:
            details = {}
            for subcontent in face.cssselect('td.rightCol div.row'):
                id = subcontent.get('id')
                if subcontent_re.search(id):
                    k = id.split('_')[-1][:-3]
                    el = subcontent.cssselect('div.value')[0]
                    parse_method_name = 'parse_' + k
                    if hasattr(self, parse_method_name):
                        v = getattr(self, parse_method_name)(el)
                    else:
                        v = normalized_element_text(el)
                    if k == name_row_key and v != self.name:
                        break
                    details[k] = v.strip()
            if name_row_key in details:
                found = True
                art_src = face.cssselect('td.leftCol img')[0].get('src')
                details['art'] = art_src
                break

        if not found:
            # Navigate to part page if able
            if len(faces) == 1 and forward and self.name in parts:
                part_page = self.__class__(parts[self.name], self.name)
                return part_page.details(forward=False)

            # Otherwise raise exception
            raise CardNotFound(u'Card \'{0}\' not found on page \'{1}\''.format(
                self.name, self.url))

        details['url'] = self.url
        m = mvid_re.search(self.url)
        if not m:
            raise Exception('Cannot get multiverseid for {0}'.format(self.name))
        details['mvid'] = m.group('id')

        other_names = parts.keys()
        if not other_names:
            for name_block in self.doc.cssselect('td.rightCol div[id$="nameRow"] div.value'):
                value = normalized_element_text(name_block)
                if value != self.name:
                    other_names.append(value)
        if other_names:
            details['other_faces'] = other_names

        return details

    def printed_card_page(self):
        print_link = self.doc.cssselect('a#cardTextSwitchLink2')[0]
        url = print_link.get('href')
        return GathererCardPrint(url)

    def languages_page(self):
        print_link = self.doc.cssselect('a#ctl00_ctl00_ctl00_MainContent_SubContent_SubContentAnchors_DetailsAnchors_LanguagesLink')[0]
        url = print_link.get('href')
        return GathererCardLanguages(url)


class GathererCardPrint(GathererCard):
    pass


def map_card_set_to_pagination(parent_page, child_page):
    child_page.card_set=parent_page.card_set


class GathererCardList(ProviderCardListPage, GathererPage):
    def __init__(self, card_set, *args, **kwargs):
        super(GathererCardList, self).__init__(card_set, *args, **kwargs)

        # Fix list url, add `output` get parameter
        parts = list(urlparse(self.url))
        query = filter(lambda s: s and not s.startswith('output='), parts[4].split('&'))
        query.append('output=compact')
        parts[4] = '&'.join(query)
        self.url = urlunparse(parts)

    @map_result_as_pages(GathererCard)
    @cache_parsed()
    def cards_list(self, names=None):
        '''Generates list of card pages. If names argument passed, fetch infor
        only for those cards.
        '''
        urls = []
        # Iterate through card item rows
        for card_item in self.doc.cssselect('tr.cardItem'):
            # Get card name block to parse card name and url
            card_link = card_item.cssselect('td.name a')[0]
            name = normalized_element_text(card_link)
            if names and name not in names:
                continue
            url = card_link.get('href')
            # Next we should parse 'printings' block. It contains card links
            # for all card releases in all sets. We will get all links for
            # current set. We should use these links because some cards might
            # have several printing in one set (e.g. Forest, High Tide)
            printings = card_item.cssselect('td.printings a')
            # Get card set acronym to identify other links from this set
            cs_name = None
            for a in printings:
                if a.get('href') == url:
                    cs_name = a.cssselect('img')[0].get('alt')
                    break
            if cs_name is None:
                raise Exception(
                    u'Cannot find any printings link for "{0}"'.format(name))
            # Get all printings links
            for a in printings:
                if a.cssselect('img')[0].get('alt') == cs_name:
                    card_info = (name, a.get('href'))
                    urls.append(card_info)
        return urls

    @map_result_as_pages(map_data=map_card_set_to_pagination)
    @cache_parsed()
    def pages(self):
        urls = []
        pagination = self.doc.cssselect('div.pagingControls a')
        if pagination:
            for page_link in pagination:
                page_url = page_link.get('href')
                if not page_url or not page_link.text.strip().isdigit():
                    continue
                urls.append(page_url)
        else:
            urls.append(self.url)
        return urls


class GathererCardLanguages(GathererPage):
    @map_result_as_pages(GathererCard)
    @cache_parsed()
    def languages(self):
        urls = []
        for lang_row in self.doc.cssselect('table.cardList tr.cardItem'):
            cells = [td for td in lang_row.iterchildren('td')]
            lang = gettext(cells[1])
            url = cells[0].getchildren()[0].get('href')
            urls.append((lang, url))
        return urls
