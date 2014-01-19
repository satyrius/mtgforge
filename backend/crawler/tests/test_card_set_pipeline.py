import unittest
from mock import patch, Mock
from crawler.pipelines import sets
from crawler.items import CardSetItem, CardItem


class BaseCardSetPipelineTest(unittest.TestCase):
    def setUp(self):
        self.spider = Mock()
        self.pipeline = sets.BaseCardSetItemPipeline()

    def test_process_item_not_implemented(self):
        item = CardSetItem()
        with self.assertRaises(NotImplementedError):
            self.pipeline.process_item(item, self.spider)

    @patch.object(sets.BaseCardSetItemPipeline, '_process_item')
    def test_item_instance(self, _process_item):
        # Process card set items
        item = CardSetItem()
        self.assertEqual(self.pipeline.process_item(item, self.spider), item)
        _process_item.assert_called_once_with(item, self.spider)

        # And skip all other items
        item = CardItem()
        _process_item.reset_mock()
        self.assertEqual(self.pipeline.process_item(item, self.spider), item)
        self.assertFalse(_process_item.called)
