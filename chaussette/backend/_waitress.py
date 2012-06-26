import socket
from waitress.server import WSGIServer
from chaussette.util import create_socket


class Server(WSGIServer):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, listener, application=None):
        host, port = listener
        sock = create_socket(host, port, self.address_family,
                                    self.socket_type)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super(Server, self).__init__(application, _sock=sock)

    def bind(self, addr):
        pass

    def serve_forever(self):
        return self.run()
