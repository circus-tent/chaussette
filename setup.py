import sys
from setuptools import setup, find_packages

install_requires=['gunicorn', 'circus']


setup(name='chausette',
      version='0.1',
      packages=find_packages(),
      description=("A WSGI Server extension for Circus -- prototype do not use"),
      author="Tarek Ziade",
      author_email="tarek@ziade.org",
      include_package_data=True,
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 1 - Planning"],
      install_requires=install_requires,
      test_requires=['nose'],
      test_suite = 'nose.collector')
