from gevent import monkey
monkey.noisy = False
monkey.patch_all()

import socket
from gevent.pywsgi import WSGIServer, WSGIHandler
from chaussette.util import create_socket


class CustomWSGIHandler(WSGIHandler):
    def __init__(self, sock, address, server, rfile=None):
        if server.address_family == socket.AF_UNIX:
            address = ['0.0.0.0']
        WSGIHandler.__init__(self, sock, address, server, rfile)


class Server(WSGIServer):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    handler_class = CustomWSGIHandler

    def __init__(self, listener, application=None, backlog=None,
                 spawn='default', log='default', handler_class=None,
                 environ=None, socket_type=None,
                 address_family=None, **ssl_args):
        if address_family:
            self.address_family = address_family
        if socket_type:
            self.socket_type = socket_type
        if handler_class:
            self.handler_class = handler_class

        host, port = listener
        self.socket = create_socket(host, port, self.address_family,
                                    self.socket_type, backlog=backlog)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = self.socket.getsockname()
        super(Server, self).__init__(self.socket, application, None, spawn,
                                     log, self.handler_class, environ,
                                     **ssl_args)
