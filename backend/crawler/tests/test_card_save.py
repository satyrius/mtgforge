from mock import Mock, patch
from django.test import TestCase

from crawler.items import CardItem
from crawler.pipelines import cards


class CardSavePipelineTest(TestCase):
    @patch.object(cards, 'get_or_create_card_face')
    @patch.object(cards, 'get_or_create_card_image')
    @patch.object(cards, 'get_or_create_card_release')
    def test_save_helpers_call(self, get_release, get_image, get_face):
        pipeline = cards.CardsPipeline()
        item = CardItem()
        with patch.dict(item, set='Theros'):
            face = Mock()
            get_face.return_value = face
            pipeline._process_item(item, Mock())
            get_face.assert_called_once_with(item)
            get_image.assert_called_once_with(item)
            get_release.assert_called_once_with(item, face.card)
