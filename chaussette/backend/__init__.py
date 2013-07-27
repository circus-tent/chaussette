from chaussette.backend import _wsgiref

_backends = {'wsgiref': _wsgiref.ChaussetteServer}

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
    from chaussette.backend import _meinheld
    _backends['meinheld'] = _meinheld.Server
except ImportError:
    pass


try:
    from chaussette.backend import _waitress
    _backends['waitress'] = _waitress.Server
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


def register(name, server):
    _backends[name] = server


def get(name):
    return _backends[name]


def backends():
    return sorted(_backends.keys())
