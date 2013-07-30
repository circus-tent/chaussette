# coding=utf-8
"""
Tests for server.py
"""
import unittest
import minimock
from chaussette.backend import backends, get
import chaussette.server


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
        self.tt = minimock.TraceTracker()

    def tearDown(self):
        """
        tearDown
        :return:
        """
        super(TestServer, self).tearDown()
        minimock.restore()

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
        mocked_backend = minimock.Mock('Backend', returns='backend_impl', tracker=self.tt)
        minimock.mock('chaussette.server.get', returns=mocked_backend, tracker=self.tt)
        server = chaussette.server.make_server('app', 'host', 'port', backend)
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
        for backend in ['gevent', 'fastgevent', 'geventwebsocket', 'socketio']:
            self.tt = minimock.TraceTracker()
            self._check_make_server_spawn(backend)
            minimock.restore()

    def _check_make_server_spawn(self, backend):
        mocked_backend = minimock.Mock('Backend', returns='backend_impl', tracker=self.tt)
        minimock.mock('chaussette.server.get', returns=mocked_backend, tracker=self.tt)
        server = chaussette.server.make_server('app', 'host', 'port', backend, spawn=5)
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
        self.assertRaises(TypeError, chaussette.server.make_server, 'app', 'host', 'port', spawn=5)
