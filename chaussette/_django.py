import os
import sys


def django_app(path, settings_module=None):
    sys.path.insert(0, os.path.abspath(path))

    if settings_module is None:
        # trying to guess is
        if 'settings.py' in os.listdir(path):
            settings_module = '%s.%s' % (os.path.split(path)[-1], 'settings')

    if settings_module is not None:
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    import django.core.handlers.wsgi
    return django.core.handlers.wsgi.WSGIHandler()
