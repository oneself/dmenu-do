

from dmenudo.coll import LRUDict

from unittest import TestCase


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
    self.assertEquals(0, len(lru))
    self.assertEquals([], lru.keys())
    self.assertEquals([], lru.items())

  def test_str(self):
    self.assertEquals('{a: 1, b: 2, c: 3}', str(self.lru))

  def test_get(self):
    self.assertEquals(1, self.lru['a'])
    self.assertEquals(2, self.lru['b'])
    self.assertEquals(3, self.lru['c'])
    self.assertRaises(KeyError, self.lru.__getitem__, 'd')

  def test_contains(self):
    self.assertTrue('a' in self.lru)
    self.assertTrue('b' in self.lru)
    self.assertTrue('c' in self.lru)
    self.assertFalse('d' in self.lru)

  def test_set(self):
    # Initial state
    self.assertEquals(3, len(self.lru))
    self.assertEquals(['a', 'b', 'c'], self.lru.keys())
    self.assertEquals([('a', 1), ('b', 2), ('c', 3)], self.lru.items())

    # Add
    self.lru['d'] = 4
    self.assertEquals(4, len(self.lru))
    self.assertEquals(['a', 'b', 'c', 'd'], self.lru.keys())
    self.assertEquals([('a', 1), ('b', 2), ('c', 3), ('d', 4)], self.lru.items())

    # Touch
    self.lru['a'] = 5
    self.assertEquals(4, len(self.lru))
    self.assertEquals(['b', 'c', 'd', 'a'], self.lru.keys())
    self.assertEquals([('b', 2), ('c', 3), ('d', 4), ('a', 5)], self.lru.items())

  def test_remove(self):
    # Remove one
    self.assertEquals(3, len(self.lru))
    del self.lru['b']
    self.assertEquals(2, len(self.lru))
    self.assertEquals(['a', 'c'], self.lru.keys())
    self.assertEquals([('a', 1), ('c', 3)], self.lru.items())

    # Remove the rest
    del self.lru['a']
    del self.lru['c']
    self.assertEquals(0, len(self.lru))
    self.assertEquals([], self.lru.keys())
    self.assertEquals([], self.lru.items())
