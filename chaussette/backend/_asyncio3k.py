import socket
import asyncio
import aiohttp_wsgi
from chaussette.util import create_socket


class Server(object):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, listener, application=None, backlog=2048,
                 socket_type=socket.SOCK_STREAM,
                 address_family=socket.AF_INET):
        self.address_family = address_family
        self.socket_type = socket_type
        host, port = listener
        self.socket = create_socket(host, port, self.address_family,
                                    self.socket_type, backlog=backlog)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.application = application
        self.backlog = backlog
        self.port = port
        self.host = host

        # P3k asyncio
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def serve_forever(self):
        aiohttp_wsgi.serve(self.application,
                           loop=self.loop,
                           port=self.port,
                           host=self.host,
                           **dict(socket=self.socket,
                                  backlog=self.backlog))
        print("Serving")