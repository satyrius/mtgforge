import re

from oracle.providers import HomePage, ProviderPage


class WizardsPage(ProviderPage):
    provider_name = 'wizards'


class WizardsHomePage(HomePage, WizardsPage):
    def products_list_generator(self):
        product_link_re = re.compile(r'x=mtg[/_]tcg[/_](?:products[/_]([^/_#]+)|([^/_]+)[/_]productinfo)$')
        cards_count_re = re.compile(r'(\d+)\s+cards', re.IGNORECASE)
        separator_re = re.compile(r'\s*(?:,|and)\s*')
        for link in self.doc.cssselect('div.article-content a'):
            href = link.get('href')
            if not href:
                continue
            match = product_link_re.search(href)
            if match:
                name = ' '.join(filter(None,
                    [re.sub(r'\s+', ' ', t).strip() for t in link.itertext()]))

                for e in link.iterancestors():
                    if e.tag == 'td':
                        cards = e.getnext()
                        break
                match_cards = cards_count_re.match(cards.text.strip())
                cards_count = match_cards and int(match_cards.group(1)) or None

                release_date = [t for t in cards.getnext().itertext()][1].strip()

                result = lambda name: (name, href, dict(cards=cards_count, release=release_date))
                if ',' in name:
                    # Comma separated editions
                    for separated_name in filter(None, separator_re.split(name)):
                        yield result(separated_name)
                else:
                    yield result(name)
