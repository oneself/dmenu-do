
from mock import Mock, DEFAULT, patch

def patch_config_parser(config):
    """Patch the ConfigParser object and return the supplied config instead."""

    class ConfigParserMock(object):
      def __init__(self, d):
          self._d = d

      def read(self, f):
        pass

      def get(self, g, k):
        return self._d[g][k]

      def items(self, g):
        return self._d[g]

    return patch('dmenudo.config.ConfigParser', lambda: ConfigParserMock(config))
