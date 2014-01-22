from mock import Mock, patch
from model_mommy.recipe import Recipe, seq, foreign_key
from django.test import TestCase

from crawler.items import CardItem
from crawler.pipelines import cards
from oracle import forms
from oracle.models import CardFace, Card, CardImage, Artist


class CardSavePipelineTest(TestCase):
    def setUp(self):
        self.card_recipe = Recipe(Card)
        self.face_recipe = Recipe(
            CardFace, name=seq('Card '), card=foreign_key(self.card_recipe))
        self.artist_recipe = Recipe(Artist, name=seq('Artist '))
        self.img_recipe = Recipe(
            CardImage, mvid=seq(0),
            scan=seq('http://gatherer.wizards.com/image'))

    @patch.object(cards, 'get_or_create_card_face')
    @patch.object(cards, 'get_or_create_card_image')
    @patch.object(cards, 'get_or_create_card_release')
    @patch.object(cards, 'save_card_face')
    @patch.object(cards, 'update_card')
    def test_save_helpers_call(self, update_card, save, get_release,
                               get_image, get_face):
        pipeline = cards.CardsPipeline()
        item = CardItem()
        with patch.dict(item, set='Theros'):
            face = Mock()
            get_face.return_value = face
            save.return_value = face
            img = Mock()
            get_image.return_value = img

            pipeline._process_item(item, Mock())
            get_face.assert_called_once_with(item)
            save.assert_called_once_with(face, item)
            update_card.assert_called_once_with(face.card, item)
            get_image.assert_called_once_with(item)
            get_release.assert_called_once_with(item, face.card, img)

    def test_get_existing_face_by_name(self):
        faces = self.face_recipe.make(_quantity=3)
        face = faces[-1]

        before = Card.objects.all().count()
        res = cards.get_or_create_card_face(CardItem(name=face.name))
        self.assertEqual(res, face)
        self.assertEqual(Card.objects.all().count(), before)

    def test_new_face_for_sibling(self):
        front_face = self.face_recipe.make()
        back_face_item = CardItem(
            name=self.face_recipe.prepare().name,
            sibling=front_face.name)

        before = Card.objects.all().count()
        res = cards.get_or_create_card_face(back_face_item)
        self.assertNotEqual(res, front_face)
        self.assertIsNone(res.id)
        self.assertEqual(res.card, front_face.card)
        self.assertEqual(Card.objects.all().count(), before)

    def test_new_card(self):
        name = self.face_recipe.prepare().name
        item = CardItem(name=name, title=u'Title for {}'.format(name))
        before = Card.objects.all().count()
        res = cards.get_or_create_card_face(item)
        self.assertIsNone(res.id)
        self.assertEqual(Card.objects.all().count(), before + 1)
        self.assertEqual(res.card.name, item['title'])

    @patch.object(forms.CardFaceForm, 'save')
    @patch.object(forms.CardFaceForm, 'is_valid', return_value=True)
    def test_save_card_face(self, is_valid, save):
        face = self.face_recipe.prepare()
        save.return_value = face
        res = cards.save_card_face(face, item=CardItem())
        self.assertEqual(res, face)
        is_valid.assert_called_once_with()
        save.assert_called_once_with()

    @patch.object(forms.CardFaceForm, 'is_valid', return_value=False)
    def test_save_invalid_card_face(self, is_valid):
        face = self.face_recipe.prepare()
        with self.assertRaises(cards.InvalidError):
            cards.save_card_face(face, item=CardItem())
        is_valid.assert_called_once_with()

    def test_update_faces_count(self):
        card = self.card_recipe.make(faces_count=1)

        # Common card
        cards.update_card(card, CardItem(title='Fire // Ice'))
        card = Card.objects.get(pk=card.pk)
        self.assertEqual(card.faces_count, 1)

        # Double faced card
        cards.update_card(card, CardItem(title='Fire // Ice', sibling='Ice'))
        card = Card.objects.get(pk=card.pk)
        self.assertEqual(card.faces_count, 2)

    @patch.object(cards, 'get_or_create_card_face')
    @patch.object(cards, 'save_card_face')
    @patch.object(cards, 'update_card', side_effect=Exception('stop'))
    def test_update_card_before_face_save(self, update_card, save, get_face):
        pipeline = cards.CardsPipeline()
        item = CardItem()
        with self.assertRaisesRegexp(Exception, '^stop$'):
            pipeline._process_item(item, Mock())
        self.assertTrue(update_card.called)
        self.assertFalse(save.called)

    def test_existing_image_by_mvid_with_new_artist(self):
        img = self.img_recipe.make(_quantity=3)[-1]
        self.assertIsNone(img.artist)
        img_before = CardImage.objects.all().count()
        art_before = Artist.objects.all().count()
        item = CardItem(
            mvid=img.mvid, artist=self.artist_recipe.prepare().name)
        res = cards.get_or_create_card_image(item)
        self.assertEqual(res, img)
        self.assertIsNotNone(res.artist)
        self.assertEqual(res.artist.name, item['artist'])
        self.assertEqual(CardImage.objects.all().count(), img_before)
        self.assertEqual(Artist.objects.all().count(), art_before + 1)

    def test_create_new_image_with_existing_artist(self):
        img1 = self.img_recipe.make(artist=self.artist_recipe.make())
        img2 = self.img_recipe.prepare()
        item2 = CardItem(
            mvid=img2.mvid, art=img2.scan, artist=img1.artist.name)
        img_before = CardImage.objects.all().count()
        art_before = Artist.objects.all().count()
        res = cards.get_or_create_card_image(item2)
        self.assertNotEqual(res, img1)
        self.assertEqual(res.mvid, img2.mvid)
        self.assertEqual(res.scan, img2.scan)
        self.assertEqual(res.artist, img1.artist)
        self.assertEqual(CardImage.objects.all().count(), img_before + 1)
        self.assertEqual(Artist.objects.all().count(), art_before)
