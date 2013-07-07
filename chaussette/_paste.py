import configparser
import logging.config
import os.path
try:
    from paste.deploy import loadapp
except ImportError:
    raise ImportError("You need to install PasteDeploy")


def paste_app(path):
    abspath = os.path.abspath(path)
    try:
        logging.config.fileConfig(abspath)
    except configparser.NoSectionError:
        pass
    return loadapp('config:%s' % abspath)
