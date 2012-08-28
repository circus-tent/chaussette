import sys
from setuptools import setup, find_packages


if not hasattr(sys, 'version_info') or sys.version_info < (2, 6, 0, 'final'):
    raise SystemExit("Chaussette requires Python 2.6 or later.")

install_requires = []

try:
    import argparse     # NOQA
except ImportError:
    install_requires.append('argparse')


with open('README.rst') as f:
    README = f.read()


setup(name='chaussette',
      version='0.5',
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
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha"],
      install_requires=install_requires,
      tests_require=['nose'],
      test_suite='nose.collector',
      entry_points="""
      [console_scripts]
      chaussette = chaussette.server:main
      """)
