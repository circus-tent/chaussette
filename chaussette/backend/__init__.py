from chaussette.backend import _wsgiref

_backends = {'wsgiref': (_wsgiref.ChaussetteServer, _wsgiref.ChaussetteHandler)}


def register(name, server, handler):
    _backends[name] = server, handler


def get(name):
    return _backends[name]
