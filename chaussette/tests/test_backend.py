try:
    import unittest2 as unittest
except ImportError:
    import unittest

import sys
from chaussette.backend import backends

IS_PYPY = hasattr(sys, 'pypy_version_info')

PY2 = ['bjoern', 'eventlet', 'fastgevent', 'gevent',
       'geventwebsocket', 'geventws4py', 'meinheld',
       'socketio', 'tornado', 'waitress',
       'wsgiref']
PYPY = ['tornado', 'waitress', 'wsgiref']
PY3 = ['meinheld', 'tornado', 'waitress', 'wsgiref']


class TestBackend(unittest.TestCase):

    def test_backends(self):
        _backends = backends()
        if sys.version_info[0] == 2:
            if IS_PYPY:
                expected = PYPY
            else:
                expected = PY2
        else:
            expected = PY3
        self.assertEqual(_backends, expected)
