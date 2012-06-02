Chaussette
----------

Chaussette is a prototype WSGI server for Circus.

It comes in two parts:

A - a module that creates a socket and publish the FD in the environ
    and run some workers as child processes
B - a module that runs a wsgi worker against the socket, by getting its FD

In Circus the idea would be to "publish sockets" like A, then
have a watcher that manages n workers from B.

For now the code just returns an "Hello World" and uses Gunicorn's http
package to read the requests and send the response.

If the experiment goes well, A could be integrated in Circus ala einhorn:
people will just configure "sockets" to be opened by Circus.

Then B could be a standalone wsgi server that just (optionaly) works
with a socket initialized from a fd passed by Circus' env.

Maybe http://pypi.python.org/pypi/bjoern could be adapted and used
for that...

