from django.http import HttpRequest
from forge.tests.base import SerpTest


class CardResourceTest(SerpTest):
    def test_rules_as_array(self):
        angel = self.face_recipe.make(
            name='Angel of Despair',
            type_line='Creature - Angel',
            rules='Flying\n'
                  'When Angel of Despair enters the battlefield, destroy '
                  'target permanent.'
        )
        self.release_recipe.make(card=angel.card)
        data = self.search(q='angel')
        card = data['objects'][0]
        rules = card['rules']
        self.assertIsInstance(rules, list)
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0], 'Flying')
        self.assertTrue(rules[0].find('destroy target permanent'))

    def test_card_image(self):
        face = self.face_recipe.make()
        uri = self.resource.get_resource_uri(face)

        # Card face has no image if it was not released
        res = self.api_client.get(uri)
        self.assertHttpOK(res)
        data = self.deserialize(res)
        self.assertNotIn('thumb', data)

        # Release card, but without art
        cr = self.release_recipe.make(card=face.card, art=None)
        self.assertHttpOK(res)
        data = self.deserialize(res)
        self.assertNotIn('thumb', data)

        # Then set art, but only with original scan url
        img = self.img_recipe.make()
        self.assertIsNotNone(img.scan)
        self.assertIsNone(img.file.name)
        cr.art = img
        cr.save()
        res = self.api_client.get(uri)
        self.assertHttpOK(res)
        data = self.deserialize(res)
        self.assertIn('thumb', data)
        self.assertEqual(data['thumb'], img.scan)

        # Emulate uploaded file
        uploaded_art = 'my/uploaded/file.jpeg'
        img.file = uploaded_art
        img.save()
        res = self.api_client.get(uri)
        self.assertHttpOK(res)
        data = self.deserialize(res)
        self.assertIn('thumb', data)
        self.assertTrue(data['thumb'].endswith(uploaded_art))

    def test_queries_count(self):
        face1, face2 = self.face_recipe.make(_quantity=2)
        self.release_recipe.make(card=face1.card)
        self.release_recipe.make(card=face2.card)

        # select count
        # select from card_face
        # select from card
        # select from card_release
        # select from card_image
        # select from card_set
        with self.assertNumQueries(6):
            res = self.resource.get_list(HttpRequest())

        self.assertHttpOK(res)
        data = self.deserialize(res)
        self.assertIn('meta', data)
        self.assertIn('total_count', data['meta'])
        self.assertEqual(data['meta']['total_count'], 2)
