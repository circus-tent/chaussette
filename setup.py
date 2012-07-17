from setuptools import setup, find_packages


install_requires = []


with open('README.rst') as f:
    README = f.read()


setup(name='chaussette',
      version='0.4',
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
      test_requires=['nose'],
      test_suite='nose.collector',
      entry_points="""
      [console_scripts]
      chaussette = chaussette.server:main
      """)
