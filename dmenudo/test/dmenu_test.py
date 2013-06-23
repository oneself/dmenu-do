
from dmenudo.dmenu import DMenu
from dmenudo.const import *
from dmenudo.config import Config
from dmenudo.history import History

from unittest import TestCase
from mock import patch
from nose.tools import eq_, ok_, raises

from testutil import Mockfile, Execmock, patch_config_parser

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

class DMenuTest(TestCase):

  @patch_config_parser(CONFIG)
  def test_main(self):
    histfile = Mockfile('''test1,FILE,/test1
test2,EXECUTABLE,test2
''')
    execmock = Execmock()
    with patch('__builtin__.file', histfile):
      with patch('dmenudo.history.execute', execmock):
        with patch('dmenudo.dmenu.Popen', execmock):
          config = Config(None)
          hist = History('test.hist', 'xdg-open')
          dmenu = DMenu(config, hist)
          dmenu.run()
          print 'execmock.commands:', execmock.commands
          print 'execmock.items:', execmock.items
          ok_(False)
