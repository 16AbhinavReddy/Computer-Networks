from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import sys

PORT = 9090

class MyHTTPReequestHandler(SimpleHTTPRequestHandler) :

    def do_GET(self):
        self.cookieHeader = self.headers.get('Cookie')
        if self.cookieHeader and 'FOO' in self.cookieHeader :
            if "index" in self.path:
                self.path = '/index.html'
            elif "page2" in self.path:
                self.path = '/Pictures.html'
        SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        self.send_my_headers()
        SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Set-Cookie", "FOO123")

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

server = ThreadingSimpleServer(('10.196.10.32', PORT), MyHTTPReequestHandler)

try:
    while 1:
        server.handle_request()
except KeyboardInterrupt:
    print('Finished')