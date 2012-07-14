import socket
import eventlet
from eventlet import wsgi
from chaussette.util import create_socket

class Server(object):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self,listener,application=None,backlog=None):
        eventlet.monkey_patch()
        host, port = listener
        self.socket = create_socket(host, port, self.address_family,
                                    self.socket_type, backlog=backlog)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.application = application

    def serve_forever(self):
        wsgi.server(self.socket,self.application)
