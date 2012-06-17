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

import os
from subprocess import Popen, PIPE
import logging as log

from util import execute, home, is_directory, is_executable

class DMenu(object):

  def __init__(self, config, history):
    self._current = None
    self._config = config
    self._history = history

  def run(self, command=''):
    '''Run the dmenu command recursively'''
    items = []
    # Figure out which items to display
    if command:
      # If current is empty, we are not walking a directory tree.  So, try and see if this is a
      # session command or a path executable.
      if not self._current:
        if command in self._history:
          log.debug('HISTORY: %s' % command)
          # This is a history command, so run it.
          self._history.execute(command)
          return
        if command in self._config.session.keys():
          log.debug('SESSION: %s' % command)
          # This is a session command, so run it.
          execute(self._config.session[command])
          return
        if command in self._config.executables:
          log.debug('EXECUTABLE: %s' % command)
          self._history.add_executable(command)
          # This is an executable, so run it.
          execute(command)
          return
      # Otherwise, we must be walking a path, so join our current path
      path = os.path.join(self._current, home(command));
      if is_directory(path):
        log.debug('DIRECTORY: %s' % command)
        # Update current path
        self._current = path
        # This is a directory, so we are going to list all child files and folders.
        items = os.listdir(path)
      elif is_executable(command):
        # This is a full path executable, so run it.
        log.debug('EXECUTABLE: %s' % command)
        execute(command, path)
        return
      else:
        # This is just a file, use mailcap and try to find the right program to run it.
        log.debug('FILE: %s' % path)
        self._history.add_file(command, path)
        execute('see "%s"' % path)
        return
    else:
      # If no command was passed in, show everything
      items = self._history.keys() + \
              self._config.folders + \
              list(self._config.session.keys()) + \
              sorted(self._config.executables)
    # Open the dmenu command
    proc = Popen(self._config.dmenu, shell=False, stdout=PIPE, stdin=PIPE)
    # Run dmenu with the items defined above
    for item in items:
      proc.stdin.write(item)
      proc.stdin.write('\n')
    command = proc.communicate()[0]
    # If we got something back, run dmenu again
    if command:
      self.run(command.strip())
