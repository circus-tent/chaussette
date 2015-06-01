from tornado.web import Application, RequestHandler
from tornado.httpserver import HTTPServer
from tornado.tcpserver import TCPServer
from tornado.wsgi import WSGIApplication

class HelloHandler(RequestHandler):
    def get(self):
        self.write(b"Hello, World\n")

class HelloServer(TCPServer):
    def handle_stream(self, stream, address):
        stream.write(b"Hello, World\n")
        stream.close()

# serve a tornado app like:
#   chaussette --backend tornado examples.tornado.app.tornadoapp
# test is with:
#   curl http://127.0.0.1:8080/
tornadoapp = Application([('/', HelloHandler)])

# serve a wsgi app:
#   chaussette --backend tornado examples.tornado.app.wsgiapp
# test is with:
#   curl http://127.0.0.1:8080/
wsgiapp = WSGIApplication([('/', HelloHandler)])

# serve a tornado HTTPServer:
#   chaussette --backend tornado examples.tornado.app.hellohttp
# test is with:
#   curl http://127.0.0.1:8080/
hellohttp = HTTPServer(tornadoapp)

# serve a tornado TCPServer:
#   chaussette --backend tornado examples.tornado.app.hellotcp
# beware this is NOT a HTTP server, test it with:
#   nc 127.0.0.1 8080
hellotcp = HelloServer()



