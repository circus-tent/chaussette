import os
import ConfigParser

from logging.config import fileConfig

try:
    from paste.deploy import loadapp
except ImportError:
    raise ImportError("You need to install PasteDeploy")


def paste_app(path):
    # Load the logging config from paste.deploy .ini, if any
    parser = ConfigParser.ConfigParser()
    parser.read([path])
    if parser.has_section('loggers'):
        config_file = os.path.abspath(path)
        fileConfig(
            config_file,
            dict(__file__=config_file, here=os.path.dirname(config_file))
        )

    return loadapp('config:%s' % os.path.abspath(path))
