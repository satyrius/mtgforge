from lxml.html import HtmlElement
from mock import patch

from crawler.models import DataProviderPage, PageState
from crawler.providers import BadPageSource, Page, NoContent
from crawler.providers.base import Gatherer, Wizards
from crawler.providers.gatherer import GathererHomePage
from crawler.providers.wizards import WizardsHomePage
from crawler.tests.helpers import get_html_fixture
from crawler.tests.providers.base import ProviderTest


class DataProvidersTest(ProviderTest):
    fixtures = ['card_set']

    def test_provider_name(self):
        self.assertEqual(Gatherer().name, 'gatherer')
        self.assertEqual(Wizards().name, 'wizards')

    def test_provider_home(self):
        self.assertEqual(Gatherer().home, Gatherer._url)
        self.assertEqual(Wizards().home, Wizards._url)

    def test_page_init(self):
        url = 'http://example.com/magic/tcg/home.html'
        p = Page(url)
        self.assertEqual(p.url, url)
        self.assertIsNone(p.name)

        name = 'Savannah'
        p = Page(url, name=name)
        self.assertEqual(p.name, name)

        name = u'Akki Lavarunner (Tok-Tok, Volcano Born)'
        p = Page(url, name=name)
        self.assertEqual(p.name, 'Tok-Tok, Volcano Born')

        with self.assertRaises(BadPageSource):
            p = Page(None)

    def test_normalize_href(self):
        p = Page('http://example.com/magic/tcg/home.html')
        self.assertEqual(p.absolute_url('/foo/bar.html'),
                         'http://example.com/foo/bar.html')
        self.assertEqual(p.absolute_url('/foo.html?x=1'),
                         'http://example.com/foo.html?x=1')
        self.assertEqual(p.absolute_url('?x=1'),
                         'http://example.com/magic/tcg/home.html?x=1')
        self.assertEqual(p.absolute_url('../foo/bar.html'),
                         'http://example.com/magic/foo/bar.html')

    @patch.object(Page, 'get_content')
    def test_get_doc(self, patched_content):
        page_content = '<html><h1>Example</h1></html>'
        patched_content.return_value = page_content

        p = Page('http://example.com/')
        # Call doc property
        doc = p.doc
        self.assertIsInstance(doc, HtmlElement)
        # Call againt and it is still the same instance
        self.assertEqual(p.doc, doc)

    def test_home_page(self):
        gatherer_page = GathererHomePage()
        gatherer = Gatherer()
        self.assertEqual(gatherer_page.url, gatherer.home)

        wizards_page = WizardsHomePage()
        wizards = Wizards()
        self.assertEqual(wizards_page.url, wizards.home)
        self.assertNotEqual(wizards_page.url, gatherer_page.url)

    @patch.object(Page, '_dowload_content')
    def test_common_page_cache(self, _dowload_content):
        page_content = get_html_fixture('gatherer_list')
        _dowload_content.return_value = page_content
        dummy_url = 'http://example.com/foo/bar.html'

        # Common page has empty provider FK
        page = Page(dummy_url)
        self.assertEqual(page.get_content(), page_content)
        cache_entry = DataProviderPage.objects.get(url=dummy_url)
        self.assertIsNone(cache_entry.provider)
        self.assertIsNone(cache_entry.name)
        self.assertEqual(cache_entry.class_name, page.__class__.__name__)

    @patch.object(Page, '_dowload_content')
    def test_cache_page_name(self, _dowload_content):
        page_content = get_html_fixture('gatherer_list')
        _dowload_content.return_value = page_content
        dummy_url = 'http://example.com/foo/bar.html'

        # Assert page name saved to cache
        title = 'The Epic Page'
        _dowload_content.return_value = page_content
        page = Page(dummy_url, name=title)
        content = page.get_content()
        self.assertIsNotNone(content)
        self.assertEqual(content, page_content)
        cache_entry = DataProviderPage.objects.get(url=dummy_url)
        self.assertEqual(cache_entry.name, title)

        # Test restoring page name from cache
        page2 = Page(dummy_url)
        self.assertEqual(page2.name, title)

    @patch.object(Page, '_dowload_content')
    def test_page_state(self, _dowload_content):
        page_content = get_html_fixture('gatherer_list')
        _dowload_content.return_value = page_content
        dummy_url = 'http://example.com/foo/bar.html'

        # Assert page name saved to cache
        _dowload_content.return_value = page_content
        page = Page(dummy_url)
        self.assertEqual(page.state, PageState.INITIAL)
        content = page.get_content()
        self.assertIsNotNone(content)
        self.assertEqual(content, page_content)

        state = PageState.PARSED
        page.change_state(state)
        self.assertEqual(page.state, state)
        cache_entry = DataProviderPage.objects.get(url=dummy_url)
        self.assertEqual(cache_entry.state, state)

        # Test restoring page state from cache
        page2 = Page(dummy_url)
        self.assertEqual(page2.state, state)

        # Test change state for page without content
        dummy_url_2 = 'http://example.com/foo/baz.html'
        page3 = Page(dummy_url_2)
        with self.assertRaises(NoContent):
            page3.change_state(state)

    @patch.object(Page, '_dowload_content')
    def test_page_cache_delete(self, _dowload_content):
        page1_content = '<html><h1>1</h1></html>'
        page2_content = '<html><h1>2</h1></html>'
        page3_content = '<html><h1>3</h1></html>'

        # Get content of gatherer home page
        _dowload_content.return_value = page1_content
        self.assertEqual(_dowload_content.call_count, 0)
        gatherer_page = GathererHomePage()
        self.assertEqual(gatherer_page.get_content(), page1_content)
        self.assertEqual(_dowload_content.call_count, 1)

        # Create gatherer page again and assert that content is from cache
        gatherer_page = GathererHomePage()
        self.assertEqual(gatherer_page.get_content(), page1_content)
        self.assertEqual(_dowload_content.call_count, 1)

        # Get content of wizards home page
        _dowload_content.return_value = page2_content
        wizards_page = WizardsHomePage()
        self.assertEqual(wizards_page.get_content(), page2_content)
        self.assertEqual(_dowload_content.call_count, 2)

        # Reset gatherer home page content cache
        _dowload_content.return_value = page3_content
        gatherer_page = GathererHomePage()
        gatherer_page.delete_cache()
        self.assertEqual(gatherer_page.get_content(), page3_content)
        self.assertEqual(_dowload_content.call_count, 3)

        # Wizards page is still cached
        wizards_page = WizardsHomePage()
        self.assertEqual(wizards_page.get_content(), page2_content)
        self.assertEqual(_dowload_content.call_count, 3)
