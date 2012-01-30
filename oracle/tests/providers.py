# -*- coding: utf-8 -*-
import StringIO

from django.test import TestCase
from mock import Mock

from oracle.models import DataProvider
from oracle.providers import WizardsProvider, GathererProvider, MagiccardsProvider


__all__ = ['DataProvidersTest']


class DataProvidersTest(TestCase):
    fixtures = ['data_provider']

    def test_normalize_href(self):
        p = WizardsProvider()
        self.assertEqual(p.absolute_url('/foo/bar.aspx'),
                         'http://wizards.com/foo/bar.aspx')
        self.assertEqual(p.absolute_url('/foo.aspx?x=1'),
                         'http://wizards.com/foo.aspx?x=1')
        self.assertEqual(p.absolute_url('?x=1'),
                         'http://wizards.com/magic/tcg/Article.aspx?x=1')
        self.assertEqual(p.absolute_url('../foo/Bar.aspx'),
                         'http://wizards.com/magic/foo/Bar.aspx')
        self.assertEqual(p.absolute_url('../foo/Bar.aspx',
                                        'http://wizards.com/magic/tcg/mtg/Article.aspx'),
                         'http://wizards.com/magic/tcg/foo/Bar.aspx')

    def test_wizards_list(self):
        p = WizardsProvider()
        p.get_page = Mock(return_value=StringIO.StringIO(_wizards_home_page))
        products = p.products_list()
        self.assertEqual(products, [
            ('Zendikar', 'http://wizards.com/magic/tcg/products.aspx?x=mtg/tcg/products/zendikar', {'cards': 249, 'release': 'October 2009'})
        ])

    def test_gatherer_list(self):
        p = GathererProvider()
        p.get_page = Mock(return_value=StringIO.StringIO(_gatherer_home_page))
        products = p.products_list()
        self.assertEqual(products, [
            ('Zendikar', 'http://gatherer.wizards.com/Pages/Search/Default.aspx?set=%5B%22Zendikar%22%5D', None)
        ])

    def test_magiccards_list(self):
        p = MagiccardsProvider()
        p.get_page = Mock(return_value=StringIO.StringIO(_magiccards_home_page))
        products = p.products_list()
        self.assertEqual(products, [
            ('Zendikar', 'http://magiccards.info/zen/en.html', {'acronym': 'zen'})
        ])

    def test_provider_factory(self):
        wizards = DataProvider.objects.get(name='wizards')
        provider = wizards.provider
        self.assertIsInstance(provider, WizardsProvider)
        # Assert that property always return the same instance
        self.assertEqual(provider, wizards.provider)

        gatherer = DataProvider.objects.get(name='gatherer')
        self.assertNotEqual(gatherer.provider, wizards.provider)

_wizards_home_page = """
<html xmlns="http://www.w3.org/1999/xhtml">
<body>
<div class="article-content">
  <div style="margin: 0 0 0 50px;">
    <hr width="430" align="left" />
    <p>
      <i>Zendikar</i> Block</p>
  </div>
  <table height="64" width="777" cellpadding="0" cellspacing="0" background="/mtg/images/tcg/products/nav/ZEN.png">
    <tr>
      <td width="355"> </td>
      <td width="170">
        <i>
          <a href="/magic/tcg/products.aspx?x=mtg/tcg/products/zendikar">Zendikar</a>
        </i>
      </td>
      <td>249 cards</td>
      <td width="95">Released <br /> October 2009</td>
      <td width="64"> </td>
    </tr>
  </table>
</div>
</body>
</html>
"""

_gatherer_home_page = """
<html xmlns="http://www.w3.org/1999/xhtml">
<body>
<select name="ctl00$ctl00$MainContent$Content$SearchControls$setAddText" id="ctl00_ctl00_MainContent_Content_SearchControls_setAddText">
    <option value=""></option>
    <option value="Zendikar">Zendikar</option>
</select>
</body>
</html>
"""

_magiccards_home_page = """
<html>
<body>
<h2>English
      <img src="http://magiccards.info/images/en.gif" alt="English" width="16" height="11">
      <small style="color: #aaa;">en</small></h2>
<table cellpadding="0" cellspacing="0" width="100%" border="0"><tbody><tr><td valign="top" width="33%" nowrap="nowrap">
<ul>
  <li>Zendikar Cycle<ul>
  <li><a href="/zen/en.html">Zendikar</a> <small style="color: #aaa;">zen</small></li>
  </ul>
</ul>
</td></tr></tbody></table>
</body>
</html>
"""
