# coding=utf-8
"""
Tests for server.py
"""
import subprocess
import sys
import time
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import minimock
import requests
import socket

from chaussette.backend import backends
import chaussette.server
from chaussette.util import configure_logger
from chaussette import logger


@unittest.skipIf(sys.version_info[0] == 3, "Not py3")
class TestServer(unittest.TestCase):
    """
    Test server.py
    """

    def setUp(self):
        """
        Setup
        :return:
        """
        super(TestServer, self).setUp()
        configure_logger(logger, 'CRITICAL')

        self.tt = minimock.TraceTracker()
        try:
            self.old = socket.socket.bind
            socket.socket.bind = lambda x, y: None
        except AttributeError:
            self.old = None

    def tearDown(self):
        """
        tearDown
        :return:
        """
        super(TestServer, self).tearDown()
        minimock.restore()
        if self.old is not None:
            socket.socket.bind = self.old

    def test_make_server(self):
        """
        Test all backends with default params
        :return:
        """

        # nose does not have great support for parameterized tests
        for backend in backends():
            self.tt = minimock.TraceTracker()
            self._check_make_server(backend)
            minimock.restore()

    def _check_make_server(self, backend):
        mocked_backend = minimock.Mock('Backend', returns='backend_impl',
                                       tracker=self.tt)
        minimock.mock('chaussette.server.get', returns=mocked_backend,
                      tracker=self.tt)
        server = chaussette.server.make_server('app', 'host', 'port',
                                               backend)
        minimock.assert_same_trace(self.tt, '\n'.join([
            "Called chaussette.server.get('%s')" % backend,
            "Called Backend(",
            "    ('host', 'port'),",
            "   'app',",
            "   address_family=2,",
            "   backlog=2048,",
            "socket_type=1)"
        ]))
        self.assertEqual(server, 'backend_impl')

    def test_make_server_spawn(self):
        """
        Check the spawn option for the backend that support it
        :return:
        """
        for backend in ['gevent', 'fastgevent', 'geventwebsocket',
                        'socketio']:
            self.tt = minimock.TraceTracker()
            self._check_make_server_spawn(backend)
            minimock.restore()

    def _check_make_server_spawn(self, backend):
        mocked_backend = minimock.Mock('Backend', returns='backend_impl',
                                       tracker=self.tt)
        minimock.mock('chaussette.server.get', returns=mocked_backend,
                      tracker=self.tt)
        server = chaussette.server.make_server('app', 'host', 'port',
                                               backend, spawn=5)
        minimock.assert_same_trace(self.tt, '\n'.join([
            "Called chaussette.server.get('%s')" % backend,
            "Called Backend(",
            "    ('host', 'port'),",
            "   'app',",
            "   address_family=2,",
            "   backlog=2048,",
            "   socket_type=1,",
            "   spawn=5)"
        ]))
        self.assertEqual(server, 'backend_impl')

    def test_make_server_spawn_fail(self):
        """
        Check the spawn option for a backend that does not support it
        :return:
        """
        self.assertRaises(TypeError, chaussette.server.make_server, 'app',
                          'host', 'port', spawn=5)


class TestMain(unittest.TestCase):
    """
    Test server.py
    """

    def setUp(self):
        super(TestMain, self).setUp()
        self.argv = list(sys.argv)
        configure_logger(logger, 'CRITICAL')

    def tearDown(self):
        super(TestMain, self).tearDown()
        sys.argv[:] = self.argv

    def _launch(self, backend):
        cmd = '%s -m chaussette.server --backend %s'
        cmd = cmd % (sys.executable, backend)
        proc = subprocess.Popen(cmd.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        time.sleep(.8)
        return proc

    def test_main(self):
        _backends = backends()

        def _handler(*args):
            try:
                self.assertEqual(status, 200, '%s returned %d' %
                                 (backend, status))
            finally:
                raise KeyboardInterrupt()

        for backend in _backends:
            resp = None
            server = self._launch(backend)
            try:
                if backend in ('socketio', 'eventlet'):
                    continue
                resp = requests.get('http://localhost:8080')
                status = resp.status_code
                self.assertEqual(status, 200, backend)
            finally:
                server.terminate()
                if resp is not None:
                    resp.connection.close()
