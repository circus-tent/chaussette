import os
import sys


def django_app(path, settings_module=None, python_path=None):
    sys.path.insert(0, os.path.abspath(path))

    if settings_module is None:
        # trying to guess is
        if 'settings.py' in os.listdir(path):
            settings_module = '%s.%s' % (os.path.split(path)[-1], 'settings')

    if settings_module is not None:
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    if python_path is not None and python_path not in sys.path:
        sys.path.insert(0, python_path)

    if path not in sys.path:
        sys.path.insert(0, path)

    import django.core.handlers.wsgi
    return django.core.handlers.wsgi.WSGIHandler()
