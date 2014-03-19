from django.test import TestCase
from mock import Mock, patch
from model_mommy import mommy
from model_mommy.recipe import Recipe, seq, foreign_key

from crawler.items import L10nItem
from crawler.pipelines import l10n
from crawler.pipelines import cards
from oracle import models as m
from oracle import forms


class CardL10nSaveTest(TestCase):
    def setUp(self):
        self.card_recipe = Recipe(m.Card)
        self.face_recipe = Recipe(
            m.CardFace, name=seq('Card '), card=foreign_key(self.card_recipe))
        self.cs_recipe = Recipe(
            m.CardSet, name=seq('Magic Set '), acronym=seq('set'))
        self.img_recipe = Recipe(
            m.CardImage, mvid=seq(0),
            scan=seq('http://gatherer.wizards.com/image'))
        self.release_recipe = Recipe(
            m.CardRelease, card=foreign_key(self.card_recipe),
            card_set=foreign_key(self.cs_recipe), card_number=seq(0),
            art=foreign_key(self.img_recipe))

    @patch.object(l10n, 'get_card_release')
    @patch.object(l10n, 'get_l10n_instance')
    @patch.object(l10n, 'save_card_l10n')
    def test_save_helpers_call(self, save_l10n, get_instance, get_release):
        get_release.return_value = release, face = Mock(), Mock()
        face_l10n = Mock()
        get_instance.return_value = face_l10n

        lang = 'Russian'
        item = L10nItem(language=lang, set='Theros')
        pipeline = l10n.L10nPipeline()
        pipeline.process_item(item, Mock())

        get_release.assert_called_once_with(item)
        get_instance.assert_called_once_with(face, release, lang)
        save_l10n.assert_called_once_with(face_l10n, item)

    @patch.object(cards, 'get_card_set')
    def test_get_by_mvid_if_no_card_number(self, get_card_set):
        cr = self.release_recipe.make()
        cf = self.face_recipe.make(card=cr.card)
        get_card_set.return_value = cr.card_set
        item = L10nItem(name='Forest', language='English',
                        mvid=str(cr.art.mvid))

        self.assertEqual(l10n.get_card_release(item), (cr, cf))
        get_card_set.assert_called_once_with(item)

    @patch.object(cards, 'get_card_set')
    def test_cannot_get_non_english_release_if_no_number(self, get_card_set):
        cr = self.release_recipe.make()
        get_card_set.return_value = cr.card_set
        item = L10nItem(name='Forest', language='Russian',
                        mvid=str(cr.art.mvid))
        with self.assertRaisesRegexp(l10n.InvalidError,
                                     'Cannot setup localization'):
            l10n.get_card_release(item)

    @patch.object(cards, 'get_card_set')
    def test_no_release(self, get_card_set):
        cr1 = self.release_recipe.make()
        cs2 = self.cs_recipe.make()
        self.assertNotEqual(cr1.card_set, cs2)

        get_card_set.return_value = cs2
        item = L10nItem(number=str(cr1.card_number))
        with self.assertRaises(m.CardRelease.DoesNotExist):
            l10n.get_card_release(item)
        get_card_set.assert_called_once_with(item)

    @patch.object(cards, 'get_card_set')
    def test_no_face(self, get_card_set):
        cr = self.release_recipe.make()
        get_card_set.return_value = cr.card_set
        item = L10nItem(number='{}z'.format(cr.card_number))
        with self.assertRaises(m.CardFace.DoesNotExist):
            l10n.get_card_release(item)
        get_card_set.assert_called_once_with(item)

    @patch.object(cards, 'get_card_set')
    def test_get_release_and_face_by_card_number(self, get_card_set):
        cr = self.release_recipe.make()
        cf = self.face_recipe.make(card=cr.card)
        get_card_set.return_value = cr.card_set
        item = L10nItem(number=str(cr.card_number))
        self.assertEqual(l10n.get_card_release(item), (cr, cf))

    def test_get_existing_instance(self):
        cr = self.release_recipe.make()
        cf = self.face_recipe.make(card=cr.card)
        cl = mommy.make(
            m.CardL10n, card_face=cf, card_release=cr, language='ru')
        self.assertEqual(l10n.get_l10n_instance(cf, cr, 'Russian'), cl)

    def test_get_new_instance(self):
        cr = self.release_recipe.make()
        cf = self.face_recipe.make(card=cr.card)
        cl = l10n.get_l10n_instance(cf, cr, 'Russian')
        self.assertIsNone(cl.id)

    def test_do_not_update_locked_cards(self):
        card = self.card_recipe.make(is_locked=True)
        cl = mommy.make(m.CardL10n, card_face__card=card,
                        card_release=self.release_recipe.make(card=card))
        with patch.object(forms.CardL10nForm, 'save') as save:
            self.assertIsNone(l10n.save_card_l10n(cl, Mock()))
            self.assertFalse(save.called)

    @patch.object(forms.CardL10nForm, 'save')
    def test_l10n_save(self, save):
        cr = self.release_recipe.make()
        cl = mommy.make(m.CardL10n, card_face__card=cr.card, card_release=cr)
        item = L10nItem(name='foo', type='bar', text='', flavor='', mvid='1')
        with patch.object(m.CardImage.objects, 'get') as get:
            get.return_value = mommy.make(m.CardImage)

            with patch.object(forms.CardL10nForm, 'is_valid') as is_valid:
                is_valid.return_value = False
                with self.assertRaises(l10n.InvalidError):
                    l10n.save_card_l10n(cl, item)
                    self.assertFalse(save.called)

            l10n.save_card_l10n(cl, item)
            self.assertTrue(save.called)
