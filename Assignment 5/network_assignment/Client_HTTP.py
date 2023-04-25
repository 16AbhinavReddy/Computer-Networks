from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import sys
port = 9090

class MyHTPPRequestHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		self.cookieHeader = self.headers.get('Cookie')
		if self.cookieHeader and "F00" in self.cookieHeader:
			if "index" in self.path:
				self.path = '/index.html'
			elif "second" in self.path:
				self.path = 'second.html'
		SimpleHTTPRequestHandler.do_GET(self)
	def end_headers(self):
		self.send_my_headers()
		SimpleHTTPRequestHandler.end_headers(self)
	def send_my_headers(self):
		self.send_header("Set-Cookie","F00123")
class ThreadingSimpleServer(ThreadingMixIn,HTTPServer):
	pass
server = ThreadingSimpleServer(('10.196.10.32',port),MyHTPPRequestHandler)
try:
	while 1:
		server.handle_request()
except KeyboardInterrupt:
	print('Finished')
		
	    

