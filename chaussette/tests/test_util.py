import unittest
import os
import socket
import tempfile

from chaussette.util import create_socket, import_string


class TestUtil(unittest.TestCase):

    def test_create_socket(self):

        # testing various options

        # regular socket
        sock = create_socket('0.0.0.0')
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

        # unix socket
        fd, path = tempfile.mkstemp()
        os.close(fd)
        sock = create_socket('unix://%s' % path)
        try:
            self.assertEqual('//' + path, sock.getsockname())
        finally:
            sock.close()
            os.remove(path)

    def test_import_string(self):
        self.assertRaises(ImportError, import_string, 'chaussette.calecon')
        imported = import_string('chaussette.tests.test_util.TestUtil')
        self.assertTrue(imported is TestUtil)
