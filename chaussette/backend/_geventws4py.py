import socket
from ws4py.server.geventserver import UpgradableWSGIHandler
from chaussette.backend._gevent import Server as GeventServer


class CustomWSGIHandler(UpgradableWSGIHandler):
    def __init__(self, sock, address, server, rfile=None):
        if server.socket_type == socket.AF_UNIX:
            address = ['0.0.0.0']
        UpgradableWSGIHandler.__init__(self, sock, address, server, rfile)


class Server(GeventServer):
    handler_class = CustomWSGIHandler
