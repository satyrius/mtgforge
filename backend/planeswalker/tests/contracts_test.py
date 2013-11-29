from unittest import TextTestRunner

from twisted.trial import unittest

from scrapy.spider import BaseSpider
from scrapy.item import Item, Field
from scrapy.contracts import ContractsManager
from scrapy.contracts.default import UrlContract

from planeswalker.contracts import ItemContract, FieldContract, MetaContract,\
    QueryContract, PartialContract


class TestItem(Item):
    name = Field()
    url = Field()


class ResponseMock(object):
    url = 'http://scrapy.org'


class TestSpider(BaseSpider):
    name = 'demo_spider'

    def item_ok(self, response):
        """ returns item with name and url
        @url http://scrapy.org
        @item_json {\
            "name": "test",\
            "url": "http://scrapy.org"\
        }
        """
        return TestItem(name='test', url=response.url)

    def item_fail(self, response):
        """ returns item with name and url
        @url http://scrapy.org
        @item_json {\
            "name": "test",\
            "url": "http://scrapy.org"\
        }
        """
        return TestItem(name='test', url='/')

    def multiline_item_data(self, response):
        """ returns item with name and url
        @url http://scrapy.org
        @item_json {\
            "name": "multi\\nline",\
            "url": "http://scrapy.org"\
        }
        """
        return TestItem(name='multi\nline', url=response.url)

    def field_ok(self, response):
        """ returns item with name and url
        @url http://scrapy.org
        @field name Anton Egorov
        """
        return TestItem(name='Anton Egorov')

    def field_fail(self, response):
        """ returns item with name and url
        @url http://scrapy.org
        @field name Anton Egorov
        """
        return TestItem(name='Anton')

    def multiline_field(self, response):
        """ returns item with name and url
        @url http://scrapy.org
        @field name Anton\\nEgorov
        """
        return TestItem(name='Anton\nEgorov')

    def field_with_empty_value(self, response):
        """ returns item with name and empty url
        @url http://scrapy.org
        @field name Anton Egorov
        @field url
        """
        return TestItem(name='Anton Egorov', url='')

    def field_with_empty_value_2(self, response):
        """ returns item with name and empty url
        @url http://scrapy.org
        @field name Anton Egorov
        @field url
        """
        return TestItem(name='Anton Egorov')

    def field_with_empty_value_fail(self, response):
        """ returns item with name and empty url
        @url http://scrapy.org
        @field name Anton Egorov
        @field url
        """
        return TestItem(name='Anton Egorov', url='/foo/bar')

    def with_meta(self, response):
        """ returns nothing
        @url http://scrapy.org
        @meta name Anton Egorov
        """
        return

    def with_query_param(self, response):
        """ returns nothing
        @url http://scrapy.org
        @url_query name Anton Egorov
        """
        return

    def partial_item_ok(self, response):
        """ returns items with name and url
        @url http://scrapy.org
        @partial {\
            "name": "docs"\
        }
        @partial {\
            "name": "github"\
        }
        """
        yield TestItem(name='docs', url="http://docs.scrapy.org")
        yield TestItem(name='github', url="https://github.com/scrapy/scrapy")

    def partial_item_fail(self, response):
        """ returns items with name and url
        @url http://scrapy.org
        @partial {\
            "name": "bitbucket"\
        }
        """
        yield TestItem(name='docs', url="http://docs.scrapy.org")
        yield TestItem(name='github', url="https://github.com/scrapy/scrapy")


class ContractsTest(unittest.TestCase):
    contracts = [
        UrlContract, ItemContract, FieldContract, MetaContract, QueryContract,
        PartialContract
    ]

    def setUp(self):
        self.conman = ContractsManager(self.contracts)
        self.results = TextTestRunner()._makeResult()
        self.results.stream = None
        self.spider = TestSpider()
        self.response = ResponseMock()

    def should_succeed(self):
        self.assertFalse(self.results.failures)
        self.assertFalse(self.results.errors)

    def should_fail(self):
        self.assertTrue(self.results.failures)
        self.assertFalse(self.results.errors)

    def test_item_json_ok(self):
        request = self.conman.from_method(self.spider.item_ok, self.results)
        output = request.callback(self.response)
        self.assertEqual([type(x) for x in output], [TestItem])
        self.should_succeed()

    def test_item_json_fail(self):
        request = self.conman.from_method(self.spider.item_fail, self.results)
        request.callback(self.response)
        self.should_fail()

    def test_multiline_item_data(self):
        request = self.conman.from_method(
            self.spider.multiline_item_data, self.results)
        output = request.callback(self.response)
        self.assertEqual([type(x) for x in output], [TestItem])
        self.should_succeed()

    def test_field_ok(self):
        request = self.conman.from_method(self.spider.field_ok, self.results)
        output = request.callback(self.response)
        self.assertEqual([type(x) for x in output], [TestItem])
        self.should_succeed()

    def test_field_fail(self):
        request = self.conman.from_method(self.spider.field_fail, self.results)
        request.callback(self.response)
        self.should_fail()

    def test_multiline_field(self):
        request = self.conman.from_method(
            self.spider.multiline_field, self.results)
        output = request.callback(self.response)
        self.assertEqual([type(x) for x in output], [TestItem])
        self.should_succeed()

    def test_field_with_empty_value(self):
        request = self.conman.from_method(
            self.spider.field_with_empty_value, self.results)
        output = request.callback(self.response)
        self.assertEqual([type(x) for x in output], [TestItem])
        self.should_succeed()

        request = self.conman.from_method(
            self.spider.field_with_empty_value_2, self.results)
        output = request.callback(self.response)
        self.assertEqual([type(x) for x in output], [TestItem])
        self.should_succeed()

    def test_field_with_empty_value_fail(self):
        request = self.conman.from_method(
            self.spider.field_with_empty_value_fail, self.results)
        request.callback(self.response)
        self.should_fail()

    def test_request_meta(self):
        request = self.conman.from_method(self.spider.with_meta, self.results)
        self.assertIn('name', request.meta)
        self.assertEqual(request.meta['name'], 'Anton Egorov')

    def test_request_query_param(self):
        request = self.conman.from_method(self.spider.with_query_param, self.results)
        self.assertEqual(request.url, 'http://scrapy.org?name=Anton+Egorov')

    def test_partial_item_json_ok(self):
        request = self.conman.from_method(
            self.spider.partial_item_ok, self.results)
        output = request.callback(self.response)
        self.assertEqual([type(x) for x in output], [TestItem, TestItem])
        self.should_succeed()

    def test_partial_item_json_fail(self):
        request = self.conman.from_method(
            self.spider.partial_item_fail, self.results)
        output = request.callback(self.response)
        self.assertEqual([type(x) for x in output], [TestItem, TestItem])
        self.should_fail()
