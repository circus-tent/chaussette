import os
import time
import sys
import socket
import tempfile


def resolve_name(name):
    """Resolve a name like ``module.object`` to an object and return it.

    This functions supports packages and attributes without depth limitation:
    ``package.package.module.class.class.function.attr`` is valid input.
    However, looking up builtins is not directly supported: use
    ``__builtin__.name``.

    Raises ImportError if importing the module fails or if one requested
    attribute is not found.
    """
    if '.' not in name:
        # shortcut
        __import__(name)
        return sys.modules[name]

    # FIXME clean up this code!
    parts = name.split('.')
    cursor = len(parts)
    module_name = parts[:cursor]
    ret = ''

    while cursor > 0:
        try:
            ret = __import__('.'.join(module_name))
            break
        except ImportError:
            cursor -= 1
            module_name = parts[:cursor]

    if ret == '':
        raise ImportError(parts[0])

    for part in parts[1:]:
        try:
            ret = getattr(ret, part)
        except AttributeError, exc:
            raise ImportError(exc)

    return ret


def hello_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return ['hello world']


def bench_app(environ, start_response):
    start = time.time()
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)

    # math
    for i in range(10000):
        10 * 1000 * 1000

    time.sleep(.1)

    # I/O
    fd, path = tempfile.mkstemp()
    for i in range(10000):
        os.write(fd, str(i))
    os.close(fd)
    os.remove(path)
    return ['%.4f' % (time.time() - start)]


def create_socket(host, port, family=socket.AF_INET, type=socket.SOCK_STREAM,
                  backlog=2048, blocking=True):
    if host.startswith('fd://'):
        # just recreate the socket
        fd = int(host.split('://')[1])
        sock = socket.fromfd(fd, family, type)
    else:
        sock = socket.socket(family, type)
        sock.bind((host, port))
        sock.listen(backlog)

    if blocking:
        sock.setblocking(1)
    else:
        sock.setblocking(0)
    return sock
