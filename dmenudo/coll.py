# Copyright (C) 2012 Eyal Erez
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not,
# write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from collections import defaultdict

class LRUDict(object):
  '''An OrderedDict allows a user to add key/value pairs, like a dict, but maintains the order of
  addition.  If an item is added more the once, it will move to the end of the list.  So, the order
  is LRU first.  (Note: this implementation is not thread-safe)
  '''

  def __init__(self, maxsize=1024):
    '''Create an empty dict'''
    self._d = {}
    self._k = []
    self._maxsize = maxsize

  def __len__(self):
    self._dedup()
    return len(self._k)

  def __getitem__(self, key):
    '''Get value'''
    return self._d[key]

  def __setitem__(self, key, value):
    '''Set value'''
    self._k.append(key)
    self._d[key] = value
    # Overflow, remove oldest
    if len(self._k) > self._maxsize:
      del self[self._k[0]]

  def __delitem__(self, key):
    '''Remove item'''
    self._k.remove(key)
    del self._d[key]

  def __contains__(self, key):
    '''Contains key'''
    return key in self._d

  def keys(self):
    '''Return list of keys in order of insertion'''
    self._dedup()
    return self._k

  def items(self):
    '''Return items as a list of (key, value) tuples'''
    self._dedup()
    items = []
    for k in self._k:
      items.append((k, self._d[k]))
    return items

  def _dedup(self):
    '''Remove all key duplicates'''
    # Count the number of duplicates
    dups = defaultdict(int)
    for k in self._k:
      dups[k] += 1
    ks = []
    for k in self._k:
      dups[k] -= 1
      if dups[k] == 0:
        ks.append(k)
    self._k = ks

  def __str__(self):
    s = []
    for k in self._k:
      s.append('%s: %s' % (k, self._d[k]))
    return '{%s}' % ', '.join(s)
