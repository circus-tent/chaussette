import socket
from waitress.server import WSGIServer


class Server(WSGIServer):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, listener, application=None, backlog=2048):
        host, port = listener
        if host.startswith('fd://'):
            self._fd = int(host.split('://')[1])
        else:
            self._fd = None

        super(Server, self).__init__(application, backlog=backlog, host=host,
                                     port=port)

    def create_socket(self, family, type):
        self.family_and_type = family, type
        if self._fd is None:
            sock = socket.socket(family, type)
        else:
            sock = socket.fromfd(self._fd, family, type)
        sock.setblocking(0)
        self.set_socket(sock)

    def serve_forever(self):
        return self.run()
