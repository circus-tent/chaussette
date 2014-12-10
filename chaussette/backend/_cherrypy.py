import cherrypy


class FileDescriptorsUnsupported(Exception):
    pass


class Server(object):
    def __init__(self, listener, application=None, backlog=2048,
                 socket_type=None, address_family=None):
        host, port = listener
        cherrypy.tree.graft(application, '/')
        cherrypy.server.unsubscribe()

        server = cherrypy._cpserver.Server()
        if host.startswith('fd://'):
            raise FileDescriptorsUnsupported
        elif host.startswith('unix://'):
            server.socket_file = host.split('unix://')[1]
        else:
            server.socket_host = host
            server.socket_port = port
        server.socket_queue_size = backlog
        server.subscribe()

    def serve_forever(self):
        cherrypy.engine.start()
        cherrypy.engine.block()
