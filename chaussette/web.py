import socket
import os
from subprocess import Popen, PIPE
import sys

# this is a "Circus Socket"
# a socket managed by circus in circusd
HOST = 'localhost'
PORT = 8081
res = socket.getaddrinfo(HOST, PORT, socket.AF_INET6, socket.SOCK_STREAM)
family, socktype, proto, canonname, sockaddr = res[1]

# creating a socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(sockaddr)
sock.listen(1)

print 'Listening to %s:%d' % (HOST, PORT)

# passing its fd in the environ
os.environ['SOCKET'] = str(sock.fileno())

python = sys.executable
here = os.path.dirname(__file__)


# creating 2 web workers now these will be managed by circus
# since they will be circusd subprocess they can share the socket
#
p = Popen(python + " worker.py", shell=True, stdout=PIPE, stderr=PIPE,
          cwd=here)
p2 = Popen(python + " worker.py", shell=True, stdout=PIPE, stderr=PIPE,
          cwd=here)


# here will just wait --
print p.stderr.read()
print p2.stderr.read()
