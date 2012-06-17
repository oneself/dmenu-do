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
from ConfigParser import ConfigParser
import logging as log
from subprocess import Popen, PIPE

from const import *
from util import home

class Config(object):

  def __init__(self, config_file):
    self._config = ConfigParser()
    self._config.read(config_file)
    # Init logging
    log.basicConfig(filename=home(self._config.get(SEC_LOGGING, OPT_FILE)),
                    level=self._config.get(SEC_LOGGING, OPT_LEVEL))
    # Get config values
    self.session = dict(self._config.items(SEC_SESSION))
    self.folders = [f.strip() for f in self._config.get(SEC_BROWSE, OPT_DIRS).split(',')]
    self.history_file = home(self._config.get(SEC_HISTORY, OPT_FILE))
    self.dmenu = [f.strip() for f in self._config.get(SEC_COMMANDS, OPT_DMENU).split(' ')]
    self._exec = [f.strip() for f in self._config.get(SEC_COMMANDS, OPT_EXEC).split(' ')]

  @property
  def executables(self):
    '''Get list of executables based on $PATH'''
    path = os.environ['PATH'].split(':')
    proc = Popen(self._exec + path, stdout=PIPE)
    lines = []
    line = proc.stdout.readline()
    while line:
      lines.append(line.strip())
      line = proc.stdout.readline()
    return lines
