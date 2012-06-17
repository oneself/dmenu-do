

from dmenudo.coll import LRUDict

from unittest import TestCase


class TestLRUDict(TestCase):

  def setUp(self):
    self.lru = LRUDict()

  def tearDown(self):
    self.lru = None

  def test_empty(self):
    self.assertEquals(0, len(self.lru))
