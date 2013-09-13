try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import sys

from tempfile import mkstemp
from chaussette._paste import paste_app


INI = """\
[composite:main]
use = egg:Paste#urlmap
/ = home

[app:home]
use = egg:Paste#static
document_root = %(here)s/htdocs
"""


@unittest.skipIf(sys.version_info[0] == 3, "Only Python 2")
class TestPasteApp(unittest.TestCase):

    def setUp(self):
        self.files = []

    def tearDown(self):
        for file_ in self.files:
            os.remove(file_)

    def _get_file(self):
        fd, path = mkstemp()
        os.close(fd)
        self.files.append(path)
        return path

    def test_app(self):
        path = self._get_file()

        with open(path, 'w') as f:
            f.write(INI)

        app = paste_app(path)
        self.assertEqual(len(app), 1)
