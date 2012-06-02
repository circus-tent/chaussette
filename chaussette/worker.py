import os
import socket
import select

from gunicorn.http import RequestParser
from gunicorn.http.wsgi import create
from gunicorn.util import close_on_exec, close


class cfg:
    limit_request_line = 8190
    limit_request_fields = 32768
    limit_request_field_size = 8190
    workers = 1
    secure_scheme_headers = []
    x_forwarded_for_header = ''


def serve():
    # getting back the fd from the env
    h = os.environ['SOCKET']

    # binding to the socket
    sock = socket.fromfd(int(h), socket.AF_INET6, socket.SOCK_STREAM)
    address = sock.getsockname()
    PIPE = os.pipe()
    timeout = 1

    while True:
        # accepting
        client, addr = sock.accept()
        client.setblocking(1)
        close_on_exec(client)

        # handling a request
        print 'Connected by', addr
        parser = RequestParser(cfg, client)
        req = parser.next()
        resp, environ = create(req, client, addr, address, cfg)
        resp.force_close()
        resp.write('Hello World, for pid %d' % os.getpid())
        resp.close()

        close(client)

        # select
        try:
            ret = select.select([sock], [], PIPE, timeout)
            if ret[0]:
                continue
        except select.error, e:
            if e[0] == errno.EINTR:
                continue
            if e[0] == errno.EBADF:
                if self.nr < 0:
                    continue
                else:
                    return
            raise


if __name__ == '__main__':
    serve()
