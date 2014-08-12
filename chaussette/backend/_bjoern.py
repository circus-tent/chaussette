import socket
from chaussette.util import create_socket
import bjoern


class Server(object):
    def __init__(self, listener, application=None, backlog=None,
                 socket_type=None, address_family=None):
        host, port = listener
        self.app = application
        self.sock = create_socket(host, port, address_family,
                                  socket_type, backlog=backlog)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def serve_forever(self):
        bjoern.server_run(self.sock, self.app)
