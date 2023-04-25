# This is the Server program that uses UDP
#
# Sequence of steps:
#	1. create a socket  
#	2. bind the socket to a host and port address
#	3. start sending and receiving data on this socket


import socket
from datetime import date
import time

#  create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# The first argument should be AF_INET
	# The second argument is SOCK_STREAM for TCP service
	#    and SOCK_DGRAM for UDP service

# bind it to a host and a port
host = '10.196.15.27'
port = 43387  # arbitrarily chosen non-privileged port number
s.bind((host,port))

print("Server started...waiting for a connection from the client")
while True:
	# receive some bytes and print them
	today = str(date.today())
	clock = time.localtime()
	clock = str(time.strftime("%H:%M:%S",clock))
	data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
	print("Server received MESSAGE=",data.decode(),"from ADDR=",addr)

	if data.decode() == "SEND_DATE":
		#send something back
		s.sendto(today.encode('utf-8'), (addr[0], addr[1]))
	if data.decode() == "SEND_TIME":
		#send something back
		s.sendto(clock.encode('utf-8'), (addr[0], addr[1]))
	if data.decode() == "q":
		#send something back
		break

	# close the connection
s.close()
