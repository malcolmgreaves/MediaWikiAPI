# -*- coding: utf-8 -*-
from decimal import Decimal
import unittest
import mediawikiapi
from mediawikiapi import MediaWikiAPI
from request_mock_data import mock_data

api = MediaWikiAPI()
# mock out _wiki_request
def _wiki_request(params, config):
  return mock_data["_wiki_request calls"][tuple(sorted(params.items()))]
# api.session.request = _wiki_request


class TestPageSetUp(unittest.TestCase):
  """Test the functionality of mediawikiapi.page's __init__ and load functions."""
  def test_missing(self):
    """Test that page raises a PageError for a nonexistant page."""
    # Callicarpa?
    purpleberry = lambda: api.page("purpleberrynotexist", auto_suggest=False)
    self.assertRaises(mediawikiapi.PageError, purpleberry)

  def test_redirect_true(self):
    """Test that a page successfully redirects a query."""
    # no error should be raised if redirect is test_redirect_true
    mp = api.page("Template:cn", auto_suggest=False)

    self.assertEqual(mp.title, "Template:Citation needed")
    self.assertEqual(mp.url, "https://en.wikipedia.org/wiki/Template:Citation_needed")

  def test_redirect_false(self):
    """Test that page raises an error on a redirect when redirect == False."""
    mp = api.page("Template:cn", auto_suggest=False, redirect=False)
    # self.assertRaises(mediawikiapi.RedirectError, mp)
    self.assertIsInstance(mp, mediawikiapi.WikipediaPage)

  def test_redirect_no_normalization(self):
    """Test that a page with redirects but no normalization query loads correctly"""
    the_party = api.page("Communist Party", auto_suggest=False)
    self.assertIsInstance(the_party, mediawikiapi.WikipediaPage)
    self.assertEqual(the_party.title, "Communist party")

  def test_redirect_with_normalization(self):
    """Test that a page redirect with a normalized query loads correctly"""
    the_party = api.page("communist Party", auto_suggest=False)
    self.assertIsInstance(the_party, mediawikiapi.WikipediaPage)
    self.assertEqual(the_party.title, "Communist party")

  def test_redirect_normalization(self):
    """Test that a page redirect loads correctly with or without a query normalization"""
    capital_party = api.page("Communist Party", auto_suggest=False)
    lower_party = api.page("communist Party", auto_suggest=False)

    self.assertIsInstance(capital_party, mediawikiapi.WikipediaPage)
    self.assertIsInstance(lower_party, mediawikiapi.WikipediaPage)
    self.assertEqual(capital_party.title, "Communist party")
    self.assertEqual(capital_party, lower_party)

  def test_disambiguate(self):
    """Test that page raises an error when a disambiguation page is reached."""
    page = api.page("Template", auto_suggest=False, redirect=False)
    disambiguation_list = [u'Template (file format)', u'Template (C++)', u'Template metaprogramming',
                           u'Template method pattern', u'Template processor', u'Template (word processing)',
                           u'Web template', u'Template (racing)', u'Template (novel)']
    for disambiguation_opt in disambiguation_list:
      self.assertTrue(disambiguation_opt in page.disambiguate_pages)

  def test_auto_suggest(self):
    """Test that auto_suggest properly corrects a typo."""
    # yum, butter.
    butterfly = api.page("butteryfly")

    self.assertEqual(butterfly.title, "Butterfly")
    self.assertEqual(butterfly.url, "https://en.wikipedia.org/wiki/Butterfly")


class TestPage(unittest.TestCase):
  """Test the functionality of the rest of mediawikiapi.page."""

  def setUp(self):
    # shortest wikipedia articles with images and sections
    self.celtuce = api.page("Celtuce")
    self.cyclone = api.page("Tropical Depression Ten (2005)")
    self.great_wall_of_china = api.page("Great Wall of China")

  def test_from_page_id(self):
    """Test loading from a page id"""
    self.assertEqual(self.celtuce, api.page(pageid=1868108))

  def test_title(self):
    """Test the title."""
    self.assertEqual(self.celtuce.title, "Celtuce")
    self.assertEqual(self.cyclone.title, "Tropical Depression Ten (2005)")

  def test_url(self):
    """Test the url."""
    self.assertEqual(self.celtuce.url, "https://en.wikipedia.org/wiki/Celtuce")
    self.assertEqual(self.cyclone.url, "https://en.wikipedia.org/wiki/Tropical_Depression_Ten_(2005)")

  def test_content(self):
    """Test the plain text content."""
    self.assertEqual(self.celtuce.content, mock_data['data']["celtuce.content"])
    self.assertEqual(self.cyclone.content, mock_data['data']["cyclone.content"])

  def test_revision_id(self):
    """Test the revision id."""
    self.assertEqual(self.celtuce.revision_id, mock_data['data']["celtuce.revid"])
    self.assertEqual(self.cyclone.revision_id, mock_data['data']["cyclone.revid"])

  def test_parent_id(self):
    """Test the parent id."""
    self.assertEqual(self.celtuce.parent_id, mock_data['data']["celtuce.parentid"])
    self.assertEqual(self.cyclone.parent_id, mock_data['data']["cyclone.parentid"])

  def test_images(self):
    """Test the list of image URLs."""
    # the assertEqual with sorting is used instead assertCountEqual for python 2 compatibility
    self.assertEqual(sorted(self.celtuce.images), sorted(mock_data['data']["celtuce.images"]))
    self.assertEqual(sorted(self.cyclone.images), sorted(mock_data['data']["cyclone.images"]))

  def test_references(self):
    """Test the list of reference URLs."""
    # the assertEqual with sorting is used instead assertCountEqual for python 2 compatibility
    self.assertEqual(sorted(self.celtuce.references), sorted(mock_data['data']["celtuce.references"]))
    self.assertEqual(sorted(self.cyclone.references), sorted(mock_data['data']["cyclone.references"]))

  def test_links(self):
    """Test the list of titles of links to Wikipedia pages."""
    # the assertEqual with sorting is used instead assertCountEqual for python 2 compatibility
    self.assertEqual(sorted(self.celtuce.links), sorted(mock_data['data']["celtuce.links"]))
    self.assertEqual(sorted(self.cyclone.links), sorted(mock_data['data']["cyclone.links"]))

  def test_html(self):
    """Test the full HTML method."""
    self.assertEqual(self.celtuce.html(), mock_data['data']["celtuce.html"])

  def test_coordinates(self):
    """Test geo coordinates of a page"""
    lat, lon = self.great_wall_of_china.coordinates
    self.assertEqual(str(lat.quantize(Decimal('1.000'))), mock_data['data']['great_wall_of_china.coordinates.lat'])
    self.assertEqual(str(lon.quantize(Decimal('1.000'))), mock_data['data']['great_wall_of_china.coordinates.lon'])

  def test_summary(self):
    """Test the summary."""
    # Strip is used to nuke \n from the end
    self.assertEqual(self.celtuce.summary.strip(), mock_data['data']["celtuce.summary"])
    self.assertEqual(self.cyclone.summary.strip(), mock_data['data']["cyclone.summary"])

  def test_categories(self):
    """Test the list of categories of Wikipedia pages."""
    # the assertEqual with sorting is used instead assertCountEqual for python 2 compatibility
    self.assertEqual(sorted(self.celtuce.categories), sorted(mock_data['data']["celtuce.categories"]))
    self.assertEqual(sorted(self.cyclone.categories), sorted(mock_data['data']["cyclone.categories"]))

  def test_sections(self):
    """Test the list of section titles."""
    # the assertEqual with sorting is used instead assertCountEqual for python 2 compatibility
    self.assertEqual(sorted(self.cyclone.sections), sorted(mock_data['data']["cyclone.sections"]))

  def test_section(self):
    """Test text content of a single section."""
    self.assertEqual(self.cyclone.section("Impact"), mock_data['data']["cyclone.section.impact"])
    self.assertEqual(self.cyclone.section("History"), None)

  def test_lang_title(self):
    """ Test lang_title function"""
    self.assertEqual(self.celtuce.lang_title('es'), mock_data['data']["celtuce.es_lang"])
    self.assertEqual(self.cyclone.lang_title('ru'), mock_data['data']["cyclone.ru_lang"])

  def test_pageprops(self):
    """Test pageprops of a page"""
    self.assertEqual(self.celtuce.pageprops, mock_data['data']["celtuce.pageprops"])
    self.assertEqual(self.cyclone.pageprops, mock_data['data']["cyclone.pageprops"])
