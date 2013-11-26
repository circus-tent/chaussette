import socket
from gevent.pywsgi import WSGIServer
from gevent import monkey
from geventwebsocket.handler import WebSocketHandler
from chaussette.util import create_socket


class Server(WSGIServer):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, listener, application=None, backlog=None,
                 spawn='default', log='default', handler_class=None,
                 environ=None, socket_type=socket.SOCK_STREAM,
                 address_family=socket.AF_INET, **ssl_args):
        self.address_family = address_family
        self.socket_type = socket_type
        monkey.noisy = False
        monkey.patch_all()
        host, port = listener
        self.handler_class = WebSocketHandler
        self.socket = create_socket(host, port, self.address_family,
                                    self.socket_type, backlog=backlog)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = self.socket.getsockname()
        super(Server, self).__init__(self.socket, application, None, spawn,
                                     log, handler_class, environ, **ssl_args)
