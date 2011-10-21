



import unittest
from wsgid.core import parser
from wsgid.core.parser import CommandLineOption, BOOL, INT, STRING, LIST
import sys
import signal
import platform

from mock import patch
from wsgid.commands import *

class ParserTest(unittest.TestCase):

  '''
    Test if we correctly parse options added by sub-commands 
    --no-daemon is added by the config command
  '''
  def test_parse_aditional_options(self):
    sys.argv[1:] = ['--no-debug', '--app-path=/tmp']
    opts = parser.parse_options()
    self.assertTrue(opts.no_debug)

  def test_parse_aditional_options_py26(self):
    with patch('platform.python_version'):
      platform.python_version.return_value = '2.6'
      # Call the parser
      sys.argv[1:] = ['--no-debug', '--app-path=/tmp']
      opts = parser.parse_options()
      self.assertTrue(opts.no_debug)

  '''
   Tests that the default signal os 15 (SIGTERM)
  '''
  def test_default_signal(self):
    sys.argv[1:] = ['--app-path=/tmp']
    opts = parser.parse_options()
    self.assertEquals(signal.SIGTERM, opts.send_signal)

  def test_parse_workers_as_integer(self):
    with patch('platform.python_version'):
      platform.python_version.return_value = '2.7.1'
      sys.argv[1:] = ['--workers=4']
      opts = parser.parse_options()
      self.assertEquals(4, opts.workers)



class CommandLineOptionTest(unittest.TestCase):


  def test_bool_default_true(self):
    opt = CommandLineOption(name="debug", type = BOOL, dest = 'debug', default_value = True)
    self.assertEquals('--debug', opt.name)
    self.assertEquals('store_true', opt.action)
    self.assertEquals('debug', opt.dest)

  def test_bool_default_false(self):
    opt = CommandLineOption(name="no-debug", type = BOOL, dest = 'nodebug', default_value = False)
    self.assertEquals('--no-debug', opt.name)
    self.assertEquals('store_false', opt.action)
    self.assertEquals('nodebug', opt.dest)

  def test_default_dest(self):
    opt = CommandLineOption(name="no-debug", type = BOOL, default_value = False)
    self.assertEquals('--no-debug', opt.name)
    self.assertEquals('store_false', opt.action)
    self.assertEquals('no_debug', opt.dest)

  def test_default_action(self):
    opt = CommandLineOption(name="no-debug", default_value = False)
    self.assertEquals('store', opt.action)

  def test_bool_correct_type(self):
    opt = CommandLineOption(name="no-debug", type = BOOL, default_value = False)
    self.assertEquals(bool, opt.type)

  def test_int_correct_type(self):
    opt = CommandLineOption(name="workers", type = INT)
    self.assertEquals(int, opt.type)
