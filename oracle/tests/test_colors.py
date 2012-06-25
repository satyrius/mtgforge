# -*- coding: utf-8 -*-
from django.test import TestCase
from oracle.models import Color


class ColorsTest(TestCase):
    w = 0b1
    u = 0b10
    b = 0b100
    r = 0b1000
    g = 0b10000
    c = 0b100000

    def test_color(self):
        # No color identiy (e.g. Lands)
        c = Color()
        self.assertEqual(c.identity, 0)
        self.assertEqual(c.colors, [])

        # White
        c = Color('w')
        self.assertEqual(c.identity, self.w)
        self.assertEqual(c.colors, [self.w])

        # Blue
        c = Color('u')
        self.assertEqual(c.identity, self.u)
        self.assertEqual(c.colors, [self.u])

        # Black
        c = Color('b')
        self.assertEqual(c.identity, self.b)
        self.assertEqual(c.colors, [self.b])

        # Red
        c = Color('r')
        self.assertEqual(c.identity, self.r)
        self.assertEqual(c.colors, [self.r])

        # Green
        c = Color('g')
        self.assertEqual(c.identity, self.g)
        self.assertEqual(c.colors, [self.g])

        # Colorless
        c = Color('1')
        self.assertEqual(c.identity, self.c)
        self.assertEqual(c.colors, [self.c])
        c = Color('x')
        self.assertEqual(c.identity, self.c)
        self.assertEqual(c.colors, [self.c])

    def test_multicolored_colors_order(self):
        gw = Color('gw')
        self.assertEqual(gw.identity, self.w | self.g)
        self.assertEqual(gw.colors, [self.w, self.g])

        wg = Color('wg')
        self.assertEqual(wg.identity, gw.identity)
        self.assertEqual(wg.colors, gw.colors)

    def test_colorless_with_colored(self):
        c = Color('1w')
        self.assertEqual(c.identity, self.w)
        self.assertEqual(c.colors, [self.w])

    def test_noise_symbols(self):
        # Costs Green and White mana
        c = Color('{g}{w}')
        self.assertEqual(c.identity, self.w | self.g)
        self.assertEqual(c.colors, [self.w, self.g])

        # Costs White or Red mana
        c = Color('{w/r}')
        self.assertEqual(c.identity, self.w | self.r)
        self.assertEqual(c.colors, [self.w, self.r])

        # Costs one Phyrexian Blue mana
        c = Color('{pu}')
        self.assertEqual(c.identity, self.u)
        self.assertEqual(c.colors, [self.u])

        # Costs two White mana
        c = Color('{w}{w}')
        self.assertEqual(c.identity, self.w)
        self.assertEqual(c.colors, [self.w])

        # Illegal sybbols in mana cost
        c = Color('{w}{w}{z}')
        self.assertEqual(c.identity, self.w)
        self.assertEqual(c.colors, [self.w])
