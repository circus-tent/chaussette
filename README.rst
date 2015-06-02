Chaussette
==========

Chaussette is a WSGI server. The particularity of Chaussette is that
it can either bind a socket on a port like any other server does or
run against already opened sockets.

That makes Chaussette the best companion to run a WSGI or Django_ stack
under a process and socket manager, such as Circus_.

.. image:: https://travis-ci.org/circus-tent/chaussette.svg?branch=master
   :alt: Build Status
   :target: https://secure.travis-ci.org/circus-tent/chaussette/

.. image:: https://coveralls.io/repos/circus-tent/chaussette/badge.svg?branch=master
   :alt: Coverage Status on master
   :target: https://coveralls.io/r/circus-tent/chaussette?branch=master

.. image:: https://img.shields.io/pypi/v/chaussette.svg
   :target: https://python.org/pypi/chaussette/

.. image:: https://img.shields.io/pypi/dm/chaussette.svg
   :target: https://python.org/pypi/chaussette/

.. image:: http://allmychanges.com/p/python/chaussette/badge/
   :target: http://allmychanges.com/p/python/chaussette/?utm_source=badge


Quick Start
-----------

Running:

.. code-block:: bash

   chaussette

starts a very simple HTTP sample server on port 8080.  


Starting a WSGI application using chaussette is simply a matter of calling:

.. code-block:: bash

   chaussette examples.tornadoapp.wsgiapp

Chaussette can also serve tornado (non WSGI) application:

.. code-block:: bash

   chaussette --backend tornado examples.tornadoapp.tornadoapp

The `simple_chat` example can be started as:

.. code-block:: bash

   chaussette --backend socketio examples.simple_chat.chat.app

Note that the two previous examples are not backend agnostic, since
they are not (pure) WSGI applications.

A flask_ based pure WSGI application can be started with most
backends:

.. code-block:: bash

   chaussette --backend gevent examples.flaskapp.app


In these examples, we start a standalone WSGI server, but the spirit of
chaussette is to be managed by Circus_, as described
http://chaussette.readthedocs.org/en/latest/#using-chaussette-in-circus

   
Links
-----

- The full documentation is located at: http://chaussette.readthedocs.org
- You can reach us for any feedback, bug report, or to contribute, at
  https://github.com/circus-tent/chaussette

.. _Circus: http://circus.readthedocs.org
.. _Django: https://docs.djangoproject.com
.. _flask: http://flask.pocoo.org/


Changelog
---------

1.3.0 - 2015-06-01
~~~~~~~~~~~~~~~~~~

- Fix gevent monkey patching (pull request #67).
- Add a "--graceful-timeout" option (for gevent-based backends).
- Fix the tornado backend so that it accepts tornado's WSGIApplication
  instaces.
- Update documentation.
- Improve example applications.


