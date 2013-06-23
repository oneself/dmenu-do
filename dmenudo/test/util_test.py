
from dmenudo.util import *

from unittest import TestCase
from nose.tools import eq_, ok_

class UtilTest(TestCase):

  def test_home(self):
    ok_('~/' != home('~/'))
    eq_('/bin', home('/bin'))

  def test_execute(self):
    execute('ls')

  def test_is_executable(self):
    ok_(is_executable('/bin/sh'))
    ok_(not is_executable('/etc/hosts'))
    ok_(not is_executable('/doesnt_exist'))

  def test_is_directory(self):
    ok_(is_directory('/bin'))
    ok_(not is_directory('/etc/hosts'))
    ok_(not is_directory('/doesnt_exist'))
