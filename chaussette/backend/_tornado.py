import socket
import tornado.ioloop
import tornado.netutil
import tornado.wsgi
from tornado.platform.auto import set_close_exec
from tornado.web import Application
from tornado.tcpserver import TCPServer
from tornado.httpserver import HTTPServer


class Server(object):
    def __init__(self, listener, application=None, backlog=2048,
                 socket_type=socket.SOCK_STREAM,
                 address_family=socket.AF_INET):
        self.address_family = address_family
        self.socket_type = socket_type
        host, port = listener

        if isinstance(application, Application):
            self._server = HTTPServer(application)
        elif isinstance(application, TCPServer):
            self._server = application
        elif callable(application):
            tapp = tornado.wsgi.WSGIContainer(application)
            self._server = HTTPServer(tapp)
        else:
            raise TypeError(
                "Unsupported application type: %r" % (application,))

        if host.startswith('fd://'):
            fd = int(host.split('://')[1])
            set_close_exec(fd)
            sock = socket.fromfd(fd, address_family, socket_type)
            sock.setblocking(0)
            socks = [sock]
        elif self.address_family == socket.AF_UNIX:
            filename = host[len('unix:'):]
            sock = tornado.netutil.bind_unix_socket(filename, backlog=backlog)
            socks = [sock]
        else:
            socks = tornado.netutil.bind_sockets(
                port, host, address_family, backlog)
        self._server.add_sockets(socks)
        self.application = application

    def serve_forever(self):
        tornado.ioloop.IOLoop.instance().start()
