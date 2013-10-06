class Provider(object):
    @property
    def name(self):
        return self.__class__.__name__.lower()

    @property
    def home(self):
        return self._url


class Gatherer(Provider):
    _url = 'http://gatherer.wizards.com/Pages/Default.aspx'


class Wizards(Provider):
    _url = 'http://wizards.com/magic/tcg/Article.aspx?x=mtg/tcg/products/allproducts'
