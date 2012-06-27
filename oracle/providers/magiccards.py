from oracle.providers import HomePage, ProviderPage


class MagiccardsPage(ProviderPage):
    name = 'magiccards'


class MagiccardsHomePage(HomePage, MagiccardsPage):
    def products_list_generator(self):
        english_header = filter(
            lambda el: el.text.strip().startswith('English'),
            self.soup.findAll('h2'))[0]

        for link in english_header.findNextSibling('table').findAll('a'):
            href = link.get('href')
            if not href:
                continue
            name = link.text.strip()
            acronym = link.findNextSibling('small').text.strip() or None
            yield name, self.absolute_url(href), dict(acronym=acronym)
