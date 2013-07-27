import os
import time
import sys
import socket
import threading
import select
import random
from six.moves import queue
import logging
import fcntl

import six


LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG}

LOG_FMT = r"%(asctime)s [%(process)d] [%(levelname)s] %(message)s"
LOG_DATE_FMT = r"%Y-%m-%d %H:%M:%S"


def close_on_exec(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    flags |= fcntl.FD_CLOEXEC
    fcntl.fcntl(fd, fcntl.F_SETFD, flags)


def configure_logger(logger, level='INFO', output="-"):
    loglevel = LOG_LEVELS.get(level.lower(), logging.INFO)
    logger.setLevel(loglevel)
    if output == "-":
        h = logging.StreamHandler()
    else:
        h = logging.FileHandler(output)
        close_on_exec(h.stream.fileno())
    fmt = logging.Formatter(LOG_FMT, LOG_DATE_FMT)
    h.setFormatter(fmt)
    logger.addHandler(h)


class ImportStringError(ImportError):
    """Provides information about a failed :func:`import_string` attempt."""

    #: String in dotted notation that failed to be imported.
    import_name = None
    #: Wrapped exception.
    exception = None

    def __init__(self, import_name, exception):
        self.import_name = import_name
        self.exception = exception

        msg = (
            'import_string() failed for %r. Possible reasons are:\n\n'
            '- missing __init__.py in a package;\n'
            '- package or module path not included in sys.path;\n'
            '- duplicated package or module name taking precedence in '
            'sys.path;\n'
            '- missing module, class, function or variable;\n\n'
            'Debugged import:\n\n%s\n\n'
            'Original exception:\n\n%s: %s')

        name = ''
        tracked = []
        for part in import_name.replace(':', '.').split('.'):
            name += (name and '.') + part
            imported = import_string(name, silent=True)
            if imported:
                tracked.append((name, getattr(imported, '__file__', None)))
            else:
                track = ['- %r found in %r.' % (n, i) for n, i in tracked]
                track.append('- %r not found.' % name)
                msg = msg % (import_name, '\n'.join(track),
                             exception.__class__.__name__, str(exception))
                break

        ImportError.__init__(self, msg)

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.import_name,
                                 self.exception)


def import_string(import_name, silent=False):
    """Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).

    If `silent` is True the return value will be `None` if the import fails.

    For better debugging we recommend the new :func:`import_module`
    function to be used instead.

    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """
    # force the import name to automatically convert to strings
    if isinstance(import_name, six.text_types):
        import_name = import_name.encode('utf-8')
    try:
        if ':' in import_name:
            module, obj = import_name.split(':', 1)
        elif '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
        else:
            return __import__(import_name)
            # __import__ is not able to handle unicode strings in the fromlist
        # if the module is a package
        if isinstance(obj, six.text_types):
            obj = obj.encode('utf-8')
        try:
            return getattr(__import__(module, None, None, [obj]), obj)
        except (ImportError, AttributeError):
            # support importing modules not yet set up by the parent module
            # (or package for that matter)
            modname = module + '.' + obj
            __import__(modname)
            return sys.modules[modname]
    except ImportError as e:
        if not silent:
            six.reraise(ImportStringError, ImportStringError(import_name, e),
                        sys.exc_info()[2])


def hello_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return ['hello world']


_IN = _OUT = None
_DBS = queue.Queue()


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
                print('nothing came back')
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
    if config.backend in ('gevent', 'fastgevent'):
        from gevent import monkey
        monkey.patch_all()
    elif config.backend == 'meinheld':
        from meinheld import patch
        patch.patch_all()

    # starting 10 threads in the background
    for i in range(10):
        th = _FakeDBThread()
        th.start()
        _DBS.put(th)

    time.sleep(0.2)


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
    if family == socket.AF_UNIX and not host.startswith('unix:'):
        raise ValueError('Your host needs to have the unix:/path form')
    if host.startswith('unix:') and family != socket.AF_UNIX:
        # forcing to unix socket family
        family = socket.AF_UNIX

    if host.startswith('fd://'):
        # just recreate the socket
        fd = int(host.split('://')[1])
        sock = socket.fromfd(fd, family, type)
    else:
        sock = socket.socket(family, type)
        if host.startswith('unix:'):
            filename = host[len('unix:'):]
            try:
                os.remove(filename)
            except OSError:
                pass
            sock.bind(filename)
        else:
            sock.bind((host, port))
        sock.listen(backlog)

    if blocking:
        sock.setblocking(1)
    else:
        sock.setblocking(0)
    return sock
