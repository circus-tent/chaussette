import os
import socket
from meinheld import server


class Server(object):
    def __init__(self, listener, application=None, backlog=2048,
                 socket_type=socket.SOCK_STREAM,
                 address_family=socket.AF_INET):
        self.address_family = address_family
        self.socket_type = socket_type
        from meinheld import patch
        patch.patch_all()
        server.set_backlog(backlog)
        host, port = listener
        if host.startswith('fd://'):
            fd = int(host.split('://')[1])
            server.set_listen_socket(fd)
        else:
            if self.address_family == socket.AF_UNIX:
                filename = listener[0][len('unix:'):]

                try:
                    os.remove(filename)
                except OSError:
                    pass
                server.listen(filename)
            else:
                server.listen(listener)

        self.application = application

    def serve_forever(self):
        server.run(self.application)
