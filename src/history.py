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

import logging as log

from coll import LRUDict
from util import execute

class History(object):

  TYPE_EXECUTABLE = "EXECUTABLE"
  TYPE_FILE       = "FILE"

  def __init__(self, filename):
    self._filename = filename
    self._commands = LRUDict()
    try:
      with file(self._filename, 'r') as reader:
        for line in reader:
          line = line.strip()
          if line:
            log.debug('READ HISTORY %s' % line)
            name, command_type, command = line.split(',')
            self._commands[name] = command_type, command
    except IOError:
      pass # file not found, this is fine, we'll just created it later.

  def add_executable(self, command):
    self._commands[command] = (self.TYPE_EXECUTABLE, command)

  def add_file(self, name, path):
    self._commands[name] = (self.TYPE_FILE, path)

  def execute(self, name):
    command_type, command = self._commands[name]
    if self.TYPE_EXECUTABLE == command_type:
      execute(command)
    elif self.TYPE_FILE == command_type:
      execute('see "%s"' % command)
    else:
      raise ValueError('Unknown command type "%s"' % command_type)
    # Pop to first place
    self._commands[name] = command_type, command

  def keys(self):
    return self._commands.keys()

  def __contains__(self, key):
    '''Contains key'''
    return key in self._commands

  def close(self):
    log.debug('CLOSING')
    log.debug('WRITING HISTORY %s' % self._filename)
    with file(self._filename, 'w+') as writer:
      for (name, (command_type, command)) in self._commands.items():
        line = "%s,%s,%s" % (name, command_type, command)
        log.debug(line)
        writer.write(line)
        writer.write('\n')
    log.debug('DONE WRITING HISTORY %s' % self._filename)
