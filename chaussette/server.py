import sys
import argparse

from chaussette.util import resolve_name
from chaussette.backend import get, backends
from chaussette._django import django_app


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
    parser.add_argument('--pre-hook', type=str, default=None)
    parser.add_argument('--post-hook', type=str, default=None)
    parser.add_argument('--django-settings', type=str, default=None)
    parser.add_argument('--python-path', type=str, default=None)
    args = parser.parse_args()

    application = args.application

    if application.startswith('django:'):
        app = django_app(application.split(':')[-1], args.django_settings,
                         args.python_path)
    else:
        app = resolve_name(application)

    if args.fd != -1:
        host = 'fd://%d' % args.fd
    else:
        host = args.host

    # pre-hook ?
    if args.pre_hook is not None:
        pre_hook = resolve_name(args.pre_hook)
        print('Running the pre-hook %r' % pre_hook)
        pre_hook(args)

    # post-hook ?
    if args.post_hook is not None:
        post_hook = resolve_name(args.post_hook)
    else:
        post_hook = None

    try:
        httpd = make_server(app, host=host, port=args.port,
                            backend=args.backend, backlog=args.backlog)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)
    finally:
        if post_hook is not None:
            print('Running the post-hook %r' % post_hook)
            post_hook(args)


if __name__ == '__main__':
    main()
