Chaussette
==========

Chaussette is a WSGI server for Circus.

It provides a web server your can launch against a WSGI application,
using the **chaussette** console script::

    $ chaussette myapp

It has a specific mode to run against an existing open socket.
This can only be used when Chaussette is forked from another process::

    $ chaussette --fd 12 myapp

Chaussette is a dead-simple runner and does not come with any fancy
processes or threads managment system.

The typical use case is to run Chaussette workers in `Circus <http://circus.io>`_,
which takes care of the sockets and spawn Chaussette workers.


Backends
--------

By default Chaussette uses a pure Python implementation based on **wsgiref**,
but it also provides more efficient back ends:

- **gevent** -- based on Gevent's *pywsgi* server
- **fastgevent**: -- based on Gevent's *wsgi* server -- faster but does not
  support streaming.
- **meinheld** -- based on Meinheld's fast C server

If you want to add your favorite WSGI Server as a backend to Chaussette,
send me mail !


Running with Circus
-------------------

To run your WSGI application using Circus, define a *socket* section in your
configuration file, then add a Chaussette worker.

Minimal example::

    [circus]
    check_delay = 5
    endpoint = tcp://127.0.0.1:5555
    pubsub_endpoint = tcp://127.0.0.1:5556
    stats_endpoint = tcp://127.0.0.1:5557

    [watcher:web]
    cmd = chaussette --fd ${socket:web} --backend meinheld server.app
    use_sockets = True
    warmup_delay = 0
    numprocesses = 5
    stdout_stream.class = StdoutStream
    stderr_stream.class = StdoutStream

    [socket:web]
    host = 0.0.0.0
    port = 8000


