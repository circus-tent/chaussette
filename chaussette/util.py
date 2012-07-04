import os
import time
import sys
import socket
import threading
import select
import random
import Queue


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


_IN = _OUT = None
_DBS = Queue.Queue()


_ITEMS = """\
<HTML>
  <BODY>
    Hello there.
  </BODY>
</HTML>""".split('\n')


class _FakeDBThread(threading.Thread):
    """Simulates a DB connection
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.read1, self.write1 = os.pipe()
        self.read2, self.write2 = os.pipe()
        self.running = False
        self.daemon = True

    def send_to_db(self, data):
        os.write(self.write1, data)

    def get_from_db(self):
        data = []
        while True:
            rl, __, __ = select.select([self.read2], [], [], 1.)
            if rl == []:
                print 'nothing came back'
                continue
            current = os.read(self.read2, 1024)
            data.append(current)
            if current.strip().endswith('</HTML>'):
                break
        return data

    def run(self):
        self.running = True
        while self.running:
            rl, __, __ = select.select([self.read1], [], [], 1.)
            if rl == []:
                continue

            os.read(self.read1, 1024)

            for item in _ITEMS:
                os.write(self.write2, item + '\n')

    def stop(self):
        self.running = False
        self.join()
        for f in (self.read1, self.read2, self.write1, self.write2):
            os.close(f)


def setup_bench(config):
    # early patch
    #if config.backend in ('gevent', 'fastgevent'):
    from gevent import monkey
    monkey.patch_all()
    #elif config.backend == 'meinheld':
    #    from meinheld import patch
    #    patch.patch_all()

    # starting 10 threads in the background
    for i in range(10):
        th = _FakeDBThread()
        th.start()
        _DBS.put(th)

    time.sleep(0.2)

setup_bench(None)


def teardown_bench(config):
    while not _DBS.empty():
        th = _DBS.get()
        th.stop()


_100BYTES = '*' * 100 + '\n'


def bench_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)

    # math
    for i in range(10000):
        10 * 1000 * 1000

    duration = float(random.randint(25, 50) + 50)
    time.sleep(duration / 1000.)

    # I/O - sending 100 bytes, getting back an HTML page
    result = []

    # picking a DB
    db = _DBS.get(timeout=1.0)
    try:
        db.send_to_db(_100BYTES)
        for line in db.get_from_db():
            result.append(line)
    finally:
        _DBS.put(db)

    return result


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
