import re
import urllib
from urlparse import urlparse, urlunparse

from contrib.soupselect import select
from oracle.providers import (
    HomePage, ProviderPage, ProviderCardListPage, ProviderCardPage,
    map_result_as_pages, cache_parsed
)


mvid_re = re.compile('multiverseid\=(?P<id>\d+)')


class GathererPage(ProviderPage):
    provider_name = 'gatherer'

    def _normalize_spaces(self, text):
        text = re.sub(r'(?<!\(|\{|\s)\{', ' {', text)
        text = re.sub(r'\}(?!=\)|\}|\s|\:)', '} ', text)
        text = re.sub(r'}\s+{', '}{', text)
        return text

    def _normalize_puct(self, text):
        text = re.sub(u'\xe2\x80\x99|\u2019', '\'', text)
        text = re.sub(u'\s*(\xe2\x80\x94|\u2014)\s*', ' - ', text)
        return text


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


class GathererCard(ProviderCardPage, GathererPage):
    def _replace_mana_img(self, img):
        mana_re = re.compile(r'name=(.+?)&')
        mana = unicode(mana_re.search(img.get('src')).groups()[0])
        img.replaceWith(u'{' + mana + u'}')

    def _encode_mana(self, html_el):
        map(self._replace_mana_img, select(html_el, 'img'))

    def parse_mana(self, html_el):
        self._encode_mana(html_el)
        return html_el.getText()

    def parse_text(self, html_el):
        blocks = []
        for block in select(html_el, 'div.cardtextbox'):
            self._encode_mana(block)
            blocks.append(block.getText())
        text = self._normalize_spaces('\n'.join(blocks))
        return self._normalize_puct(text)

    def details(self, name, oracle_text=True):
        '''Fetch cards details from page by given `url`. Use `name` to choose
        cards face or flip'''
        card_page_soup = self.soup

        found = False
        subcontent_re = re.compile('MainContent_SubContent_SubContent')
        name_row_key = 'name'
        to_normalize = ['name', 'text', 'type']
        for face in select(card_page_soup, 'table.cardDetails'):
            details = {}
            for subcontent in select(face, 'td.rightCol div.row'):
                id = subcontent.get('id')
                if subcontent_re.search(id):
                    k = id.split('_')[-1][:-3]
                    el = select(subcontent, 'div.value')[0]
                    parse_method_name = 'parse_' + k
                    if hasattr(self, parse_method_name):
                        v = getattr(self, parse_method_name)(el)
                    else:
                        v = el.getText()
                    if k in to_normalize:
                        v = self._normalize_puct(v)
                    if k == name_row_key and v != name:
                        break
                    details[k] = v.strip()
            if name_row_key in details:
                found = True
                art_src = select(face, 'td.leftCol img')[0].get('src')
                details['art'] = self.absolute_url(art_src)
                break

        if not found:
            raise CardNotFound(u'Card \'{0}\' not found on page \'{1}\''.format(
                name, self.url))

        details['url'] = self.url
        m = mvid_re.search(self.url)
        if not m:
            raise Exception('Cannot get multiverseid for {0}'.format(name))
        details['mvid'] = m.group('id')

        if oracle_text:
            printed_rulings_url = select(card_page_soup, '#cardTextSwitchLink2')[0].get('href')
            card_print_page = GathererCard(self.absolute_url(printed_rulings_url))
            printed_details = card_print_page.details(name=name, oracle_text=False)
            printed_details['oracle'] = details
            details = printed_details

        other_names = []
        for name_block in select(card_page_soup, 'td.rightCol div[id$="nameRow"] div.value'):
            value = self._normalize_spaces(name_block.getText())
            if value != name:
                other_names.append(value)
        if other_names:
            details['other_faces'] = other_names

        return details


class GathererCardPrint(GathererCard):
    pass


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
    @cache_parsed('cards')
    def cards_list(self, names=None):
        '''Generates list of card pages. If names argument passed, fetch infor
        only for those cards.
        '''
        urls = []
        for card_link in self.doc.cssselect('tr.cardItem td.name a'):
            name = self._normalize_puct(card_link.text.strip())
            if names and name not in names:
                continue
            urls.append((name, self.absolute_url(card_link.get('href'))))
        return urls

    @map_result_as_pages()
    @cache_parsed('pagination')
    def pages(self):
        urls = []
        pagination = self.doc.cssselect('div.pagingControls a')
        if pagination:
            for page_link in pagination:
                page_url = page_link.get('href')
                if not page_url or not page_link.text.strip().isdigit():
                    continue
                urls.append(self.absolute_url(page_url))
        else:
            urls.append(self.url)
        return urls


class GathererCardLanguages(GathererPage):
    pass
