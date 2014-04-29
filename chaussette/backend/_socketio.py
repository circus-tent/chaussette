import socket

from chaussette.util import create_socket

from socketio.server import SocketIOServer
from socketio.handler import SocketIOHandler
from socketio.policyserver import FlashPolicyServer


class _SocketIOHandler(SocketIOHandler):
    def __init__(self, config, sock, address, server, rfile=None):
        if server.socket_type == socket.AF_UNIX:
            address = ['0.0.0.0']
        SocketIOHandler.__init__(self, config, sock, address, server, rfile)


class Server(SocketIOServer):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    handler_class = _SocketIOHandler

    def __init__(self, *args, **kwargs):
        address_family = kwargs.pop('address_family', socket.AF_INET)
        socket_type = kwargs.pop('socket_type', socket.SOCK_STREAM)
        backlog = kwargs.pop('backlog', 2048)

        listener = args[0]
        if isinstance(listener, tuple):
            host, port = listener
            _socket = create_socket(host, port, address_family,
                                    socket_type, backlog=backlog)
            _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            args = [_socket] + list(args[1:])
        else:
            # it's already a socket..
            host, port = listener.getsockname()

        # socketio makes the assumption that listener is a host/port
        # tuple, which is a false assumption, it can be a socket.
        # it uses listener in its constructor to set the policy server
        #
        # Let's set it ourselves here afterwards.
        old_policy_server = kwargs.pop('policy_server', True)
        kwargs['policy_server'] = False
        super(Server, self).__init__(*args, **kwargs)

        if old_policy_server:
            policylistener = kwargs.pop('policy_listener', (host, 10843))
            self.policy_server = FlashPolicyServer(policylistener)
