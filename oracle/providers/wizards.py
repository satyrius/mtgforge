import re

from contrib.soupselect import select
from oracle.providers import HomePage, ProviderPage


class WizardsPage(ProviderPage):
    name = 'wizards'


class WizardsHomePage(HomePage, WizardsPage):
    def products_list_generator(self):
        product_link_re = re.compile(r'x=mtg[/_]tcg[/_](?:products[/_]([^/_]+)|([^/_]+)[/_]productinfo)$')
        cards_count_re = re.compile(r'(\d+)\s+cards', re.IGNORECASE)
        separator_re = re.compile(r'\s*(?:,|and)\s*')
        for link in select(self.soup, 'div.article-content a'):
            href = link.get('href')
            if not href:
                continue
            match = product_link_re.search(href)
            if match:
                name = re.sub(r'\s+', ' ', link.getText(u' ')).strip()

                cards = link.findParent('td').findNextSibling('td')
                match_cards = cards_count_re.match(cards.text.strip())
                cards_count = match_cards and int(match_cards.group(1)) or None

                release = cards.findNextSibling('td').find('br').nextSibling.strip()
                release_date = release or None

                url = self.absolute_url(href)
                result = lambda name: (name, url, dict(cards=cards_count, release=release_date))
                if ',' in name:
                    # Comma separated editions
                    for separated_name in filter(None, separator_re.split(name)):
                        yield result(separated_name)
                else:
                    yield result(name)
