import sys
import argparse

from chaussette.util import resolve_name
from chaussette.backend import get, backends


def make_server(app, host=None, port=None, backend='wsgiref', backlog=2048):
    print('Application is %r' % app)
    if host.startswith('fd://'):
        print('Serving on %s' % host)
    else:
        print('Serving on %s:%s' % (host, port))

    server_class = get(backend)
    print('Using %r as a backend' % server_class)
    server = server_class((host, port), app, backlog=backlog)
    return server


def main():
    parser = argparse.ArgumentParser(description='Run some watchers.')
    parser.add_argument('--port', type=int, default=8080)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--host', default='localhost')
    group.add_argument('--fd', type=int, default=-1)
    group.add_argument('--backlog', type=int, default=2048)
    parser.add_argument('--backend', type=str, default='wsgiref',
                        choices=backends())
    parser.add_argument('application', default='chaussette.util.hello_app',
                        nargs='?')
    args = parser.parse_args()

    app = resolve_name(args.application)

    if args.fd != -1:
        host = 'fd://%d' % args.fd
    else:
        host = args.host

    httpd = make_server(app, host=host, port=args.port, backend=args.backend,
                        backlog=args.backlog)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
