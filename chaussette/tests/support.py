try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import functools
import sys
from chaussette import logger


def hush(func):
    """Make the passed function silent."""
    @functools.wraps(func)
    def _silent(*args, **kw):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        debug = []

        def _debug(msg):
            debug.append(str(msg))

        old_debug = logger.debug
        logger.debug = _debug
        try:
            return func(*args, **kw)
        except:
            sys.stdout.seek(0)
            print(sys.stdout.read())
            sys.stderr.seek(0)
            print(sys.stderr.read())
            print('\n'.join(debug))
            raise
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            logger.debug = old_debug
    return _silent
