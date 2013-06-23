

from dmenudo.coll import LRUDict

from unittest import TestCase
from nose.tools import eq_, ok_, raises


class LRUDictTest(TestCase):

  def setUp(self):
    self.lru = LRUDict()
    self.lru['a'] = 1
    self.lru['b'] = 2
    self.lru['c'] = 3

  def tearDown(self):
    self.lru = None

  def test_empty(self):
    lru = LRUDict()
    eq_(0, len(lru))
    eq_([], lru.keys())
    eq_([], lru.items())

  def test_str(self):
    eq_('{a: 1, b: 2, c: 3}', str(self.lru))

  @raises(KeyError)
  def test_get(self):
    eq_(1, self.lru['a'])
    eq_(2, self.lru['b'])
    eq_(3, self.lru['c'])
    self.lru['d'] # raises KeyError

  def test_contains(self):
    ok_('a' in self.lru)
    ok_('b' in self.lru)
    ok_('c' in self.lru)
    ok_('d' not in self.lru)

  def test_set(self):
    # Initial state
    eq_(3, len(self.lru))
    eq_(['a', 'b', 'c'], self.lru.keys())
    eq_([('a', 1), ('b', 2), ('c', 3)], self.lru.items())

    # Add
    self.lru['d'] = 4
    eq_(4, len(self.lru))
    eq_(['a', 'b', 'c', 'd'], self.lru.keys())
    eq_([('a', 1), ('b', 2), ('c', 3), ('d', 4)], self.lru.items())

    # Touch
    self.lru['a'] = 5
    eq_(4, len(self.lru))
    eq_(['b', 'c', 'd', 'a'], self.lru.keys())
    eq_([('b', 2), ('c', 3), ('d', 4), ('a', 5)], self.lru.items())

  def test_remove(self):
    # Remove one
    eq_(3, len(self.lru))
    del self.lru['b']
    eq_(2, len(self.lru))
    eq_(['a', 'c'], self.lru.keys())
    eq_([('a', 1), ('c', 3)], self.lru.items())

    # Remove the rest
    del self.lru['a']
    del self.lru['c']
    eq_(0, len(self.lru))
    eq_([], self.lru.keys())
    eq_([], self.lru.items())

  def test_max_size(self):
    self.lru = LRUDict(maxsize=3)
    self.lru['a'] = 1
    self.lru['b'] = 2
    self.lru['c'] = 3
    eq_(3, len(self.lru))
    self.lru['d'] = 4
    eq_(3, len(self.lru))
    eq_([('b', 2), ('c', 3), ('d', 4)], self.lru.items())
