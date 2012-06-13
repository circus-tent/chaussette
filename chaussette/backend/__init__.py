from chaussette.backend import _wsgiref

_backends = {'wsgiref': _wsgiref.ChaussetteServer}

try:
    from chaussette.backend import _gevent
    _backends['gevent'] = _gevent.Server
except ImportError:
    pass

def register(name, server):
    _backends[name] = server


def get(name):
    return _backends[name]
