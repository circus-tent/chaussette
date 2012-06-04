Chaussette
----------

Chaussette is a prototype WSGI server for Circus.

It provides a web server your can launch against a WSGI application,
using the **chaussette** console script::

    $ chaussette myapp

It has a specific mode to run against an existing open socket.
This can only be used when chaussette is forked from another process.

The typical use case is to run chaussette workers in Circus,
which takes care of the sockets and spawn chaussette workers.

Planned: implement a backend against a performant web server
like meinheild or bjoern.
