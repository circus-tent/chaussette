import sys
from chaussette.backend import _wsgiref


_backends = {'wsgiref': _wsgiref.ChaussetteServer}

try:
    from chaussette.backend import _waitress
    _backends['waitress'] = _waitress.Server
except ImportError:
    pass

try:
    from chaussette.backend import _meinheld
    _backends['meinheld'] = _meinheld.Server
except ImportError:
    pass

try:
    from chaussette.backend import _tornado
    _backends['tornado'] = _tornado.Server
except ImportError:
    pass


try:
    from chaussette.backend import _asyncio3k
    _backends['asyncio3k'] = _asyncio3k.Server
except ImportError as e:
    print(e)


PY3 = sys.version_info[0] == 3

if not PY3:
    try:
        from chaussette.backend import _gevent
        _backends['gevent'] = _gevent.Server

        from chaussette.backend import _fastgevent
        _backends['fastgevent'] = _fastgevent.Server
    except ImportError:
        pass

    try:
        from chaussette.backend import _geventwebsocket
        _backends['geventwebsocket'] = _geventwebsocket.Server
    except ImportError:
        pass

    try:
        from chaussette.backend import _geventws4py
        _backends['geventws4py'] = _geventws4py.Server
    except ImportError:
        pass

    try:
        from chaussette.backend import _eventlet
        _backends['eventlet'] = _eventlet.Server
    except ImportError:
        pass

    try:
        from chaussette.backend import _socketio
        _backends['socketio'] = _socketio.Server
    except ImportError:
        pass

    try:
        from chaussette.backend import _bjoern
        _backends['bjoern'] = _bjoern.Server
    except ImportError:
        pass


def register(name, server):
    _backends[name] = server


def get(name):
    return _backends[name]


def backends():
    return sorted(_backends.keys())


def is_gevent_backend(backend):
    return backend in ('gevent', 'fastgevent', 'geventwebsocket',
                       'geventws4py')
