import sys
import os
import socket
import argparse


from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler
from SocketServer import BaseServer

from chaussette.util import resolve_name


class ChaussetteServer(WSGIServer):
    """WSGI Server that can reuse an existing open socket.
    """
    def __init__(self, server_address, RequestHandlerClass,
                 bind_and_activate=True):
        BaseServer.__init__(self, server_address, RequestHandlerClass)
        host, port = self.server_address = server_address
        if host.startswith('fd://'):
            self.byfd = True
            self.fd = int(host.split('://')[1])
            self.socket = socket.fromfd(self.fd, self.address_family,
                                        self.socket_type)
        else:
            self.byfd = False
            self.socket = socket.socket(self.address_family,
                                        self.socket_type)
            self.fd = self.socket.fileno()

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
            self.socket.bind(self.server_address)
            self.server_address = self.socket.getsockname()
            host, port = self.socket.getsockname()[:2]
            self.server_name = socket.getfqdn(host)
            self.server_port = port
        else:
            # XXX see how to get the fqnd with the fd
            self.server_name = self.server_address[0]
            self.server_port = self.server_address[1]

        self.setup_environ()


class ChaussetteHandler(WSGIRequestHandler):

    def address_string(self):
        return 'FD'     # XXX see how to do this


def make_server(app, host=None, port=None, fd=None,
                server_class=ChaussetteServer,
                handler_class=ChaussetteHandler):
    print('Application is %r' % app)
    if host.startswith('fd://'):
        print('Serving on %s' % host)
    else:
        print('Serving on %s:%s' % (host, port))

    server = server_class((host, port), handler_class)
    server.set_app(app)
    return server


def main():
    parser = argparse.ArgumentParser(description='Run some watchers.')
    parser.add_argument('--port', type=int, default=8080)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--host', default='localhost')
    group.add_argument('--fd', type=int, default=-1)
    parser.add_argument('application', default='chaussette.util.hello_app',
                        nargs='?')
    args = parser.parse_args()

    app = resolve_name(args.application)

    if args.fd != -1:
        host = 'fd://%d' % args.fd
    else:
        host = args.host

    httpd = make_server(app, host=host, port=args.port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
