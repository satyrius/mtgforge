from forge.tests.base import SerpTest


class SearchTest(SerpTest):
    def test_rules_as_array(self):
        self.create_card(
            name='Angel of Despair',
            type_line='Creature - Angel',
            rules='Flying\n'
                  'When Angel of Despair enters the battlefield, destroy '
                  'target permanent.'
        )
        data = self.search(q='angel')
        card = data['objects'][0]
        rules = card['rules']
        self.assertIsInstance(rules, list)
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0], 'Flying')
        self.assertTrue(rules[0].find('destroy target permanent'))
