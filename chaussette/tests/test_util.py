import unittest
import os
import socket

from chaussette.util import create_socket


class TestUtil(unittest.TestCase):

    def test_create_socket(self):

        # testing various options

        # regular socket
        sock = create_socket('0.0.0.0', 0)
        try:
            _, port = sock.getsockname()
            self.assertNotEqual(port, 0)
        finally:
            sock.close()

        # fd-based socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 0))
        _, port = sock.getsockname()

        sock2 = create_socket('fd://%d' % sock.fileno())
        try:
            _, port2 = sock2.getsockname()
            self.assertEqual(port2, port)
        finally:
            sock2.close()
            sock.close()
