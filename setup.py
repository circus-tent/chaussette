import sys
from setuptools import setup, find_packages
from chaussette import __version__


if (not hasattr(sys, 'version_info')
        or sys.version_info < (2, 6, 0, 'final')
        or (sys.version_info > (3,)
            and sys.version_info < (3, 3, 0, 'final'))):
    raise SystemExit("Chaussette requires Python 2.6, 2.7, 3.3 or later.")

PYPY = hasattr(sys, 'pypy_version_info')
PY26 = (2, 6, 0, 'final') <= sys.version_info < (2, 7, 0, 'final')

install_requires = ['six >= 1.3.0']
if PY26:
    install_requires.append('ordereddict')

try:
    import argparse     # NOQA
except ImportError:
    install_requires.append('argparse')


with open('README.rst') as f:
    README = f.read()


tests_require = ['nose', 'waitress', 'tornado',
                 'requests', 'minimock']

if not PYPY:
    tests_require += ['meinheld', 'greenlet']

if sys.version_info[0] == 2:
    tests_require += ['PasteDeploy', 'Paste', 'unittest2', 'ws4py']
    if not PYPY:
        tests_require += ['gevent', 'gevent-websocket', 'eventlet',
                          'gevent-socketio', 'bjoern']

setup(name='chaussette-backport',
      version=__version__,
      url='https://chaussette.readthedocs.io',
      packages=find_packages(exclude=['examples', 'examples.simple_chat']),
      description=("A WSGI Server for Circus"),
      long_description=README,
      author="Mozilla Foundation & Contributors",
      author_email="services-dev@lists.mozila.org",
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "License :: OSI Approved :: Apache Software License",
          "Development Status :: 3 - Alpha"],
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='nose.collector',
      entry_points="""
      [console_scripts]
      chaussette = chaussette.server:main

      [paste.server_runner]
      main = chaussette.server:serve_paste
      """)
