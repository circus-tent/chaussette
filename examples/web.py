import socket
import os
from subprocess import Popen, PIPE
import sys

HOST = 'localhost'
PORT = 8085

# creating a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

print 'Listening to %s:%d' % (HOST, PORT)

here = '/Users/tarek/Dev/github.com/chaussette'

cmd = ('/Users/tarek/Dev/github.com/chaussette/uwsgi/uwsgi --http-socket fd://%d '
       '-w chaussette.util:hello_app --logto /tmp/ok' % (sock.fileno()))


p = Popen(cmd, cwd=here, shell=True)
p2 = Popen(cmd, cwd=here, shell=True)

try:
    p.wait()
    p2.wait()
except KeyboardInterrupt:
    p.terminate()
    p2.terminate()
