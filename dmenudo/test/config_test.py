
from testutil import patch_config_parser

from dmenudo.const import *
from dmenudo.config import Config

from mock import patch
import ConfigParser

from unittest import TestCase
from nose.tools import ok_


CONFIG = {
  SEC_LOGGING: {
    OPT_FILE: '',
    OPT_LEVEL: '' },
  SEC_SESSION: {},
  SEC_BROWSE: {
    OPT_DIRS: '' },
  SEC_HISTORY: {
    OPT_FILE: '' },
  SEC_COMMANDS: {
    OPT_DMENU: '',
    OPT_EXEC: 'dmenu_path' }
  }

class ConfigTest(TestCase):

  @patch_config_parser(CONFIG)
  def test_init(self):
    config = Config(None)
    ok_(not config is None)

  @patch_config_parser(CONFIG)
  def test_executables(self):
    config = Config(None)
    ok_('ls' in config.executables)
