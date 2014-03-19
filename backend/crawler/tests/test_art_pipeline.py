from django.conf import settings
from django.test import TestCase
from mock import Mock, patch
from model_mommy.recipe import Recipe, seq
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.item import Item

from crawler.items import CardItem
from crawler.pipelines.art import CardImagePipeline
from oracle.models import CardImage


class CardImagePipelineTest(TestCase):
    def setUp(self):
        self.pipeline = CardImagePipeline(settings.MEDIA_ROOT)
        self.img_recipe = Recipe(
            CardImage, mvid=seq(0),
            scan=seq('http://gatherer.wizards.com/image?multiverseid='))

    def test_return_nothing_if_no_art_field(self):
        res = self.pipeline.get_media_requests(Item(), Mock())
        self.assertEqual(list(res), [])

    def test_remove_image_rotate(self):
        url = 'http://gatherer.wizards.com/Handlers/Image.ashx?'\
              'multiverseid=27165&type=card&options=rotate90'
        request = self.pipeline.get_media_requests(
            CardItem(art=url), Mock()).next()
        self.assertIsInstance(request, Request)
        self.assertEqual(
            request.url,
            'http://gatherer.wizards.com/Handlers/Image.ashx?'
            'multiverseid=27165&type=card')

    def test_only_one_image_allowed(self):
        results = [
            (True, {'checksum': '2b00042f7481c7b056c4b410d28f33cf',
                    'path': 'full/7d97e98f8af710c7e7fe703abc8f639e0ee507c4.jpg',
                    'url': 'http://www.example.com/images/art1.jpg'}),
            (True, {'checksum': 'b9628c4ab9b595f72f280b90c4fd093d',
                    'path': 'full/1ca5879492b8fd606df1964ea3c1e2f4520f076f.jpg',
                    'url': 'http://www.example.com/images/art2.jpg'}),
        ]
        with self.assertRaisesRegexp(DropItem, 'cannot contain more'):
            self.pipeline.item_completed(results, Item(), Mock()).next()

    @patch.object(CardImagePipeline, '_save_file')
    def test_url_without_mvid(self, save_file):
        results = [(True, {
            'checksum': '2b00042f7481c7b056c4b410d28f33cf',
            'path': 'full/7d97e98f8af710c7e7fe703abc8f639e0ee507c4.jpg',
            'url': 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card',
        })]
        with self.assertRaisesRegexp(DropItem, 'not contain multiverse id'):
            self.pipeline.item_completed(results, CardItem(), Mock())
        self.assertFalse(save_file.called)

    @patch.object(CardImagePipeline, '_save_file')
    def test_existing_image_by_mvid(self, save_file):
        img = self.img_recipe.make(_quantity=3)[-1]
        before = CardImage.objects.all().count()
        path = 'full/7d97e98f8af710c7e7fe703abc8f639e0ee507c4.jpg'
        results = [(True, {
            'checksum': '2b00042f7481c7b056c4b410d28f33cf',
            'path': path, 'url': img.scan,
        })]
        self.pipeline.item_completed(results, CardItem(), Mock())
        save_file.assert_called_once_with(img, path)
        self.assertEqual(CardImage.objects.all().count(), before)

    @patch.object(CardImagePipeline, '_save_file')
    def test_create_new_image(self, save_file):
        img1 = self.img_recipe.make()
        img2 = self.img_recipe.prepare()  # do not save!
        self.assertNotEqual(img1.scan, img2.scan)
        before = CardImage.objects.all().count()
        path = 'full/7d97e98f8af710c7e7fe703abc8f639e0ee507c4.jpg'
        results = [(True, {
            'checksum': '2b00042f7481c7b056c4b410d28f33cf',
            'path': path, 'url': img2.scan,
        })]
        self.pipeline.item_completed(results, CardItem(), Mock())
        self.assertEqual(CardImage.objects.all().count(), before + 1)
        saved = CardImage.objects.get(mvid=img2.mvid)
        self.assertEqual(saved.scan, img2.scan)
        save_file.assert_called_once_with(saved, path)
