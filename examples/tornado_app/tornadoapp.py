from tornado.web import Application, RequestHandler
from tornado.tcpserver import TCPServer


class HelloHandler(RequestHandler):
    def get(self):
        self.write(b"Hello, World\n")

helloapp = Application([('/', HelloHandler)])


class HelloServer(TCPServer):
    def handle_stream(self, stream, address):
        stream.write(b"Hello, World\n")
        stream.close()


helloserver = HelloServer()
