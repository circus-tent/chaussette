import socket
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
from SocketServer import BaseServer

from chaussette.util import create_socket


class ChaussetteHandler(WSGIRequestHandler):

    def address_string(self):
        return 'FD'     # XXX see how to do this


class ChaussetteServer(WSGIServer):
    """WSGI Server that can reuse an existing open socket.
    """
    handler_class = ChaussetteHandler

    def __init__(self, server_address, app, bind_and_activate=True):
        BaseServer.__init__(self, server_address, self.handler_class)
        self.set_app(app)

        host, port = self.server_address = server_address
        self.socket = create_socket(host, port, self.address_family,
                                    self.socket_type)
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
