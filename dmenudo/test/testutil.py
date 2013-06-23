
from mock import patch

class ConfigParserMock(object):
  def __init__(self, d):
    self._d = d

  def read(self, f):
    pass

  def get(self, g, k):
    return self._d[g][k]

  def items(self, g):
    return self._d[g]

def patch_config_parser(config):
  """Patch the ConfigParser object and return the supplied config instead."""
  return patch('dmenudo.config.ConfigParser', lambda: ConfigParserMock(config))

class Mockfile(object):

  def __init__(self, data=''):
    self._data = data.split('\n')

  def __call__(self, *args, **kwargs):
    if 'w+' in args:
      self._data = []
    return self

  def __enter__(self, *args, **kwargs):
    return self

  def __exit__(self, *args, **kwargs):
    pass

  def __iter__(self):
    return iter(self._data)

  def write(self, d):
    self._data.append(d)

  @property
  def data(self):
    return ''.join(self._data)

class Execmock(object):

  def __init__(self):
    self.commands = []
    self.items = []

  def __call__(self, *args, **kwargs):
    if len(args) == 1:
      self.commands.append(args[0])
    return self

  @property
  def stdin(self):
    return self

  def write(self, item):
    if item != '\n':
      self.items.append(item)

  def communicate(self):
    return ['']
