import socket
#from gevent.pywsgi import WSGIServer
from gevent.wsgi import WSGIServer
from gevent import monkey

monkey.noisy = False
monkey.patch_all()


class Server(WSGIServer):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, listener, application=None, backlog=None,
                 spawn='default', log='default', handler_class=None,
                 environ=None, **ssl_args):

        host, port = listener
        if host.startswith('fd://'):
            # just recreate the socket
            self.byfd = True
            self.fd = int(host.split('://')[1])
            self.socket = socket.fromfd(self.fd, self.address_family,
                                        self.socket_type)
        else:
            # bind + listen
            self.byfd = False
            self.socket = socket.socket(self.address_family,
                                        self.socket_type)
            self.fd = self.socket.fileno()
            self.socket.bind(listener)
            self.socket.listen(socket.SOMAXCONN)

        self.server_address = self.socket.getsockname()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(0)

        log = None
        super(Server, self).__init__(self.socket, application, backlog, spawn, log,
                                     handler_class, environ, **ssl_args)

