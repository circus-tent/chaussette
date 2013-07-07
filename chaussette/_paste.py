import os.path
try:
    from paste.deploy import loadapp
except ImportError:
    raise ImportError("You need to install PasteDeploy")


def paste_app(path):
    return loadapp('config:%s' % os.path.abspath(path))
