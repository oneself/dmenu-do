
from dmenudo.history import History

from unittest import TestCase
from mock import patch
from nose.tools import eq_, ok_, raises

from testutil import Mockfile, Execmock

class HistoryTest(TestCase):

  def test_create_empty(self):
    histfile = Mockfile()
    hist = History('test.hist', 'xdg-open')
    eq_([], hist.keys())
    ok_('test' not in hist)

  def test_create(self):
    histfile = Mockfile('''test1,FILE,/test1
test2,EXECUTABLE,test2
''')
    with patch('__builtin__.file', histfile):
      hist = History('test.hist', 'xdg-open')
      eq_(['test1', 'test2'], hist.keys())
      ok_('test1' in hist)
      hist.close()
      eq_('''test1,FILE,/test1
test2,EXECUTABLE,test2
''', histfile.data)

  def test_add_executable(self):
    histfile = Mockfile()
    with patch('__builtin__.file', histfile):
      hist = History('test.hist', 'xdg-open')
      hist.add_executable('test')
      eq_(['test'], hist.keys())
      ok_('test' in hist)
      hist.close()
      eq_('''test,EXECUTABLE,test
''', histfile.data)

  def test_add_file(self):
    histfile = Mockfile()
    with patch('__builtin__.file', histfile):
      hist = History('test.hist', 'xdg-open')
      hist.add_file('test', '/test')
      eq_(['test'], hist.keys())
      ok_('test' in hist)
      hist.close()
      eq_('''test,FILE,/test
''', histfile.data)

  def test_execute(self):
    histfile = Mockfile('''test1,FILE,/test1
test2,EXECUTABLE,test2
test3,EXECUTABLE,test3
''')
    execmock = Execmock()
    with patch('__builtin__.file', histfile):
      with patch('dmenudo.history.execute', execmock):
        hist = History('test.hist', 'xdg-open')
        eq_(['test1', 'test2', 'test3'], hist.keys())
        hist.execute('test1')
        eq_(['test2', 'test3', 'test1'], hist.keys())
        hist.execute('test2')
        eq_(['test3', 'test1', 'test2'], hist.keys())
        hist.close()
        eq_('''test3,EXECUTABLE,test3
test1,FILE,/test1
test2,EXECUTABLE,test2
''', histfile.data)
        eq_(['xdg-open "/test1"', 'test2'], execmock.commands)

  @raises(ValueError)
  def test_unknown_command_type(self):
    histfile = Mockfile('''test1,UNKNOWN,test1''')
    with patch('__builtin__.file', histfile):
      hist = History('test.hist', 'xdg-open')
      eq_(['test1'], hist.keys())
      hist.execute('test1')
