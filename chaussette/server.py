import sys
import os
import argparse
import socket

from chaussette import logger as chaussette_logger
from chaussette.util import import_string, configure_logger, LOG_LEVELS
from chaussette.backend import get, backends


def make_server(app, host=None, port=None, backend='wsgiref', backlog=2048,
                logger=None, address_family=socket.AF_INET,
                socket_type=socket.SOCK_STREAM):
    logger = logger or chaussette_logger
    logger.info('Application is %r' % app)
    if host.startswith('fd://') or host.startswith('unix:'):
        logger.info('Serving on %s' % host)
    else:
        logger.info('Serving on %s:%s' % (host, port))

    server_class = get(backend)
    logger.info('Using %r as a backend' % server_class)
    server = server_class((host, port), app, backlog=backlog,
                          address_family=address_family,
                          socket_type=socket_type)
    return server


_ADDRESS_FAMILY = {
    'AF_UNIX': socket.AF_UNIX,
    'AF_INET': socket.AF_INET,
    'AF_INET6': socket.AF_INET6
}

_SOCKET_TYPE = {
    'SOCK_STREAM': socket.SOCK_STREAM,
    'SOCK_DGRAM': socket.SOCK_DGRAM,
    'SOCK_RAW': socket.SOCK_RAW,
    'SOCK_RDM': socket.SOCK_RDM,
    'SOCK_SEQPACKET': socket.SOCK_SEQPACKET
}

_NO_UNIX = ('waitress', 'fastgevent', 'eventlet')


def main():
    sys.path.append(os.curdir)

    parser = argparse.ArgumentParser(description='Run some watchers.')
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--address-family', type=str, default='AF_INET',
                        choices=_ADDRESS_FAMILY.keys())
    parser.add_argument('--socket-type', type=str, default='SOCK_STREAM',
                        choices=_SOCKET_TYPE.keys())
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--host', default='localhost')
    group.add_argument('--fd', type=int, default=-1)

    group.add_argument('--backlog', type=int, default=2048)
    parser.add_argument('--backend', type=str, default='wsgiref',
                        choices=backends())
    parser.add_argument('application', default='chaussette.util.hello_app',
                        nargs='?')
    parser.add_argument('--pre-hook', type=str, default=None)
    parser.add_argument('--post-hook', type=str, default=None)
    parser.add_argument('--python-path', type=str, default=None)

    log_levels = LOG_LEVELS.keys() + [key.upper() for key in LOG_LEVELS.keys()]
    parser.add_argument('--log-level', dest='loglevel', default='info',
                        choices=log_levels, help="log level")

    parser.add_argument('--log-output', dest='logoutput', default='-',
                        help="log output")
    args = parser.parse_args()

    application = args.application

    logger = chaussette_logger
    configure_logger(logger)

    if application.startswith('paste:'):
        from chaussette._paste import paste_app
        app = paste_app(application.split(':')[-1])
    else:
        app = import_string(application)

    if args.fd != -1:
        host = 'fd://%d' % args.fd
    else:
        host = args.host

    # pre-hook ?
    if args.pre_hook is not None:
        pre_hook = import_string(args.pre_hook)
        logger.info('Running the pre-hook %r' % pre_hook)
        pre_hook(args)

    # post-hook ?
    if args.post_hook is not None:
        post_hook = import_string(args.post_hook)
    else:
        post_hook = None

    address_family = _ADDRESS_FAMILY[args.address_family]
    if address_family == socket.AF_UNIX and args.backend in _NO_UNIX:
        logger.info('Sorry %r does not support unix sockets' % args.backend)
        sys.exit(0)

    try:
        httpd = make_server(app, host=host, port=args.port,
                            backend=args.backend, backlog=args.backlog,
                            logger=logger,
                            address_family=address_family,
                            socket_type=_SOCKET_TYPE[args.socket_type])
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)
    finally:
        if post_hook is not None:
            logger.info('Running the post-hook %r' % post_hook)
            post_hook(args)


if __name__ == '__main__':
    main()
