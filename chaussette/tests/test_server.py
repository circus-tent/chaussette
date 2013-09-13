# coding=utf-8
"""
Tests for server.py
"""
import signal
import sys
import unittest
import minimock
from threading import Thread
import requests
import time
import socket

from chaussette.backend import backends
import chaussette.server
from chaussette.server import main
from chaussette.util import configure_logger
from chaussette import logger


class ThreadedServer(Thread):

    def __init__(self, backend):
        Thread.__init__(self)
        self.backend = backend

    def run(self):
        sys.argv[:] = ['chaussette', '--backend', self.backend,
                       '--log-level', 'CRITICAL']
        try:
            main()
        except Exception:
            pass


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

    def test_main(self):

        if sys.version_info[0] == 2:
            from gevent import monkey
            monkey.patch_all()

        _backends = backends()
        def _handler(*args):
            raise KeyboardInterrupt()


        for backend in _backends:
            server = ThreadedServer(backend)
            status = -1
            signal.signal(signal.SIGALRM, _handler)
            signal.alarm(1)

            try:
                server.start()
                time.sleep(.5)
                status = requests.get('http://localhost:8080').status_code
            except KeyboardInterrupt:
                pass

            self.assertEqual(status, 200)
