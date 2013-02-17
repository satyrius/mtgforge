# -*- coding: utf-8 -*-
from django.test import TestCase
from oracle.models import CardType
from oracle.utils import parse_type_line


class TypesParseTest(TestCase):
    def test_parse_basic_land(self):
        types = parse_type_line('basic land')
        assert len(types) == 2

        t = types[0]
        assert t.name == 'Basic'
        assert t.category == CardType.SUPERTYPE

        t = types[1]
        assert t.name == 'Land'
        assert t.category == CardType.TYPE

    def test_complex_type(self):
        types = parse_type_line('legendary creature - human knight')
        assert len(types) == 4

        t = types[0]
        assert t.name == 'Legendary'
        assert t.category == CardType.SUPERTYPE

        t = types[1]
        assert t.name == 'Creature'
        assert t.category == CardType.TYPE

        t = types[2]
        assert t.name == 'Human'
        assert t.category == CardType.SUBTYPE

        t = types[3]
        assert t.name == 'Knight'
        assert t.category == CardType.SUBTYPE
