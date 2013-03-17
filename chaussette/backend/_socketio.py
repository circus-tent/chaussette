import socket

from chaussette.util import create_socket

from socketio.server import SocketIOServer
from socketio.handler import SocketIOHandler
from gevent.pywsgi import WSGIServer


class _SocketIOHandler(SocketIOHandler):
    def __init__(self, sock, address, server, rfile=None):
        if server.socket_type == socket.AF_UNIX:
            address = ['0.0.0.0']
        SocketIOHandler.__init__(self, sock, address, server, rfile)


class Server(SocketIOServer):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    handler_class = _SocketIOHandler

    def __init__(self, listener, application=None, backlog=2048,
                 socket_type=socket.SOCK_STREAM, spawn='default',
                 handler_class=None, environ=None,
                 log='default', address_family=socket.AF_INET, **config):
        self.address_family = address_family
        self.socket_type = socket_type
        host, port = listener
        self.socket = create_socket(host, port, self.address_family,
                                    self.socket_type, backlog=backlog)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.application = application
        self.sockets = {}
        if 'namespace' in config:
            self.resource = config.pop('namespace', 'socket.io')
        else:
            self.resource = config.pop('resource', 'socket.io')

        self.transports = config.pop('transports', None)
        self.policy_server = None
        WSGIServer.__init__(self, self.socket, application, None, spawn,
                            log, self.handler_class, environ, **config)
