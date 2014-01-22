from mock import Mock, patch
from model_mommy.recipe import Recipe, seq, foreign_key
from django.test import TestCase

from crawler.items import CardItem
from crawler.models import CardSetAlias
from crawler.pipelines import cards
from oracle import forms
from oracle import models as m


class CardSavePipelineTest(TestCase):
    def setUp(self):
        self.card_recipe = Recipe(m.Card)
        self.face_recipe = Recipe(
            m.CardFace, name=seq('Card '), card=foreign_key(self.card_recipe))
        self.artist_recipe = Recipe(m.Artist, name=seq('Artist '))
        self.img_recipe = Recipe(
            m.CardImage, mvid=seq(0),
            scan=seq('http://gatherer.wizards.com/image'))
        self.release_recipe = Recipe(m.CardRelease, card_number=seq(0))
        self.cs_recipe = Recipe(
            m.CardSet, name=seq('Magic Set '), acronym=seq('set'))

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

        before = m.Card.objects.all().count()
        res = cards.get_or_create_card_face(CardItem(name=face.name))
        self.assertEqual(res, face)
        self.assertEqual(m.Card.objects.all().count(), before)

    def test_new_face_for_sibling(self):
        front_face = self.face_recipe.make()
        back_face_item = CardItem(
            name=self.face_recipe.prepare().name,
            sibling=front_face.name)

        before = m.Card.objects.all().count()
        res = cards.get_or_create_card_face(back_face_item)
        self.assertNotEqual(res, front_face)
        self.assertIsNone(res.id)
        self.assertEqual(res.card, front_face.card)
        self.assertEqual(m.Card.objects.all().count(), before)

    def test_new_card(self):
        name = self.face_recipe.prepare().name
        item = CardItem(name=name, title=u'Title for {}'.format(name))
        before = m.Card.objects.all().count()
        res = cards.get_or_create_card_face(item)
        self.assertIsNone(res.id)
        self.assertEqual(m.Card.objects.all().count(), before + 1)
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
        card = m.Card.objects.get(pk=card.pk)
        self.assertEqual(card.faces_count, 1)

        # Double faced card
        cards.update_card(card, CardItem(title='Fire // Ice', sibling='Ice'))
        card = m.Card.objects.get(pk=card.pk)
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
        img_before = m.CardImage.objects.all().count()
        art_before = m.Artist.objects.all().count()
        item = CardItem(
            mvid=img.mvid, artist=self.artist_recipe.prepare().name)
        res = cards.get_or_create_card_image(item)
        self.assertEqual(res, img)
        self.assertIsNotNone(res.artist)
        self.assertEqual(res.artist.name, item['artist'])
        self.assertEqual(m.CardImage.objects.all().count(), img_before)
        self.assertEqual(m.Artist.objects.all().count(), art_before + 1)

    def test_create_new_image_with_existing_artist(self):
        img1 = self.img_recipe.make(artist=self.artist_recipe.make())
        img2 = self.img_recipe.prepare()
        item2 = CardItem(
            mvid=img2.mvid, art=img2.scan, artist=img1.artist.name)
        img_before = m.CardImage.objects.all().count()
        art_before = m.Artist.objects.all().count()
        res = cards.get_or_create_card_image(item2)
        self.assertNotEqual(res, img1)
        self.assertEqual(res.mvid, img2.mvid)
        self.assertEqual(res.scan, img2.scan)
        self.assertEqual(res.artist, img1.artist)
        self.assertEqual(m.CardImage.objects.all().count(), img_before + 1)
        self.assertEqual(m.Artist.objects.all().count(), art_before)

    def test_get_release_by_mvid(self):
        img = self.img_recipe.make()
        card = self.card_recipe.make()
        release = self.release_recipe.make(art=img, card=card)
        item = CardItem(mvid=img.mvid)
        before = m.CardRelease.objects.all().count()
        res = cards.get_or_create_card_release(item, card, img)
        self.assertEqual(res, release)
        self.assertEqual(m.CardRelease.objects.all().count(), before)

        # Wrong card should raise exception
        with self.assertRaisesRegexp(cards.InvalidError, 'Card release'):
            wrong_card = self.card_recipe.make()
            cards.get_or_create_card_release(item, wrong_card, img)

    @patch.object(cards, 'get_card_set')
    def test_get_release_by_card_and_number(self, get_cs):
        cs = self.cs_recipe.make()
        card = self.card_recipe.make()
        img_b = self.img_recipe.make()
        release = self.release_recipe.make(card_set=cs, card=card)
        self.assertIsNone(release.art)
        get_cs.return_value = cs
        item = CardItem(set=cs.name, number=str(release.card_number) + 'b')
        before = m.CardRelease.objects.all().count()
        res = cards.get_or_create_card_release(
            item, card, img_b)
        self.assertEqual(m.CardRelease.objects.all().count(), before)
        get_cs.assert_called_once_with(item)
        self.assertEqual(res, release)
        self.assertEqual(res.art, img_b)

        # Update image for front face
        img_a = self.img_recipe.make()
        item = CardItem(set=cs.name, number=str(release.card_number) + 'a')
        res = cards.get_or_create_card_release(
            item, card, img_a)
        self.assertEqual(res, release)
        self.assertEqual(res.art, img_a)

        # But do not update if it is not front face
        item = CardItem(set=cs.name, number=str(release.card_number) + 'b')
        res = cards.get_or_create_card_release(
            item, card, img_b)
        self.assertEqual(res, release)
        self.assertEqual(res.art, img_a)  # Still front face image

    @patch.object(cards, 'get_card_set')
    def test_create_new_release(self, get_cs):
        cs = self.cs_recipe.make()
        card = self.card_recipe.make()
        img = self.img_recipe.make()
        get_cs.return_value = cs
        new_release = self.release_recipe.prepare()
        item = CardItem(
            set=cs.name, rarity=new_release.rarity,
            number=str(new_release.card_number))
        before = m.CardRelease.objects.all().count()
        res = cards.get_or_create_card_release(
            item, card, img)
        get_cs.assert_called_once_with(item)
        self.assertIsNotNone(res)
        self.assertEqual(res.card_set, cs)
        self.assertEqual(res.card, card)
        self.assertEqual(res.art, img)
        self.assertEqual(res.card_number, int(item['number']))
        self.assertEqual(res.rarity, item['rarity'])
        self.assertEqual(m.CardRelease.objects.all().count(), before + 1)

    def test_get_card_set(self):
        cs = self.cs_recipe.make()
        recipe = Recipe(CardSetAlias, card_set=cs, name=seq('Alias '))
        alias1 = recipe.make()

        # Find card set by alias name
        res = cards.get_card_set(CardItem(set=alias1.name))
        self.assertEqual(res, cs)

        # Raise exception if cannot find
        with self.assertRaisesRegexp(cards.InvalidError, 'card set'):
            cards.get_card_set(CardItem(set=recipe.prepare().name))
