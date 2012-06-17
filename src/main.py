#!/usr/bin/env python

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

from optparse import OptionParser

from config import Config
from history import History
from dmenu import DMenu
from const import *

def main(config_file):
  '''main method'''
  config = Config(config_file)
  history = History(config.history_file)
  try:
    dmenu = DMenu(config, history)
    dmenu.run()
  finally:
    history.close()

if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option("-c", "--config", dest="config_file",
                    help="Location of configuration file (defaults to %s" % CONFIG_FILE,
                    metavar="FILE", default=CONFIG_FILE)

  (options, args) = parser.parse_args()

  main(options.config_file)
