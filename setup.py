import sys
from setuptools import setup, find_packages
from chaussette import __version__


if (not hasattr(sys, 'version_info')
        or sys.version_info < (2, 6, 0, 'final')
        or (sys.version_info > (3,)
            and sys.version_info < (3, 3, 0, 'final'))):
    raise SystemExit("Chaussette requires Python 2.6, 2.7, 3.3 or later.")

install_requires = ['six >= 1.3.0']

try:
    import argparse     # NOQA
except ImportError:
    install_requires.append('argparse')


with open('README.rst') as f:
    README = f.read()

tests_require = ['nose', 'minimock', 'PasteDeploy', 'Paste']

if sys.version_info[0] == 2:
    tests_require.append('unittest2')


setup(name='chaussette',
      version=__version__,
      url='http://chaussette.readthedocs.org',
      packages=find_packages(),
      description=("A WSGI Server for Circus"),
      long_description=README,
      author="Mozilla Foundation & Contributors",
      author_email="services-dev@lists.mozila.org",
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
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
