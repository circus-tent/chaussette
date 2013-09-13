from ws4py.server.geventserver import (WebSocketWSGIHandler,
                                       GEventWebSocketPool)
from chaussette.backend._gevent import Server as GeventServer


class Server(GeventServer):
    handler_class = WebSocketWSGIHandler

    def __init__(self, *args, **kwargs):
        GeventServer.__init__(self, *args, **kwargs)
        self.pool = GEventWebSocketPool()

    def stop(self, *args, **kwargs):
        self.pool.clear()
        self.pool = None
        GeventServer.stop(self, *args, **kwargs)
