try:
    import unittest2 as unittest
except ImportError:
    import unittest

import sys
from chaussette.backend import backends


PY2 = ['eventlet', 'fastgevent', 'gevent',
       'geventwebsocket', 'geventws4py', 'meinheld',
       'socketio', 'waitress',
       'wsgiref']
PY3 = ['meinheld', 'waitress', 'wsgiref']


class TestBackend(unittest.TestCase):

    def test_backends(self):
        _backends = backends()
        if sys.version_info[0] == 2:
            self.assertEqual(_backends, PY2)
        else:
            self.assertEqual(_backends, PY3)
