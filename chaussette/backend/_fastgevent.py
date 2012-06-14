import socket
from gevent.wsgi import WSGIServer
from gevent import monkey
from chaussette.util import create_socket


monkey.noisy = False
monkey.patch_all()


class Server(WSGIServer):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, listener, application=None, backlog=None,
                 spawn='default', log='default', handler_class=None,
                 environ=None, **ssl_args):
        host, port = listener
        self.socket = create_socket(host, port, self.address_family,
                                    self.socket_type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = self.socket.getsockname()
        log = None
        super(Server, self).__init__(self.socket, application, backlog, spawn,
                                     log, handler_class, environ, **ssl_args)
