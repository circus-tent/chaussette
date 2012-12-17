import socket
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
from SocketServer import BaseServer

from chaussette.util import create_socket


class ChaussetteHandler(WSGIRequestHandler):
    def __init__(self, sock, client_addr, server):
        if server.socket_type == socket.AF_UNIX:
            client_addr = ['0.0.0.0']
        WSGIRequestHandler.__init__(self, sock, client_addr, server)

    def address_string(self):
        if self.server.byfd or self.server.socket_type == socket.AF_UNIX:
            return '0.0.0.0'
        return WSGIRequestHandler.address_string(self)


class ChaussetteServer(WSGIServer):
    """WSGI Server that can reuse an existing open socket.
    """
    handler_class = ChaussetteHandler

    def __init__(self, server_address, app, bind_and_activate=True,
                 backlog=2048, socket_type=socket.SOCK_STREAM,
                 address_family=socket.AF_INET):
        self.address_family = address_family
        self.socket_type = socket_type
        BaseServer.__init__(self, server_address, self.handler_class)
        self.set_app(app)

        host, port = self.server_address = server_address
        self.socket = create_socket(host, port,
                                    family=self.address_family,
                                    type=self.socket_type,
                                    backlog=backlog)
        self.byfd = host.startswith('fd://')
        if bind_and_activate:
            self.server_bind()
            self.server_activate()

    def server_activate(self):
        if self.byfd:
            return
        self.socket.listen(self.request_queue_size)

    def server_bind(self):
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if not self.byfd:
            self.server_address = self.socket.getsockname()
            host, port = self.socket.getsockname()[:2]
            self.server_name = socket.getfqdn(host)
            self.server_port = port
        else:
            # XXX see how to get the fqnd with the fd
            self.server_name = self.server_address[0]
            self.server_port = self.server_address[1]

        self.setup_environ()
