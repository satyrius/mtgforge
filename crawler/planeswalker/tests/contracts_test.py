from unittest import TextTestRunner

from twisted.trial import unittest

from scrapy.spider import BaseSpider
from scrapy.item import Item, Field
from scrapy.contracts import ContractsManager
from scrapy.contracts.default import UrlContract

from planeswalker.contracts import ItemContract


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


class ContractsTest(unittest.TestCase):
    contracts = [UrlContract, ItemContract]

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
