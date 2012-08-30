from oracle.providers import HomePage, ProviderPage


class MagiccardsPage(ProviderPage):
    provider_name = 'magiccards'


class MagiccardsHomePage(HomePage, MagiccardsPage):
    def products_list_generator(self):
        english_header = filter(
            lambda el: el.text.strip().startswith('English'),
            self.doc.cssselect('h2'))[0]

        for link in english_header.getnext().cssselect('a'):
            href = link.get('href')
            if not href:
                continue
            name = link.text.strip()
            acronym = link.getnext().text.strip() or None
            yield name, href, dict(acronym=acronym)
