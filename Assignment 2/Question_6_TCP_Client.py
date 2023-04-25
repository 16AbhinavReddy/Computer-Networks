# This is the client program

# Sequence:
#
# 1. Create a socket
# 2. Connect it to the server process. 
#	We need to know the server's hostname and port.
# 3. Send and receive data 

import socket

# create a socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# The first argument AF_INET specifies the addressing family (IP addresses)
	# The second argument is SOCK_STREAM for TCP service
	#    and SOCK_DGRAM for UDP service


# connect to the server
host='10.196.15.27'
port=43389  # this is the server's port number, which the client needs to know
s.connect((host,port))


client_name = input("Enter your name: ")

# send some bytes
s.send(client_name.encode('utf-8'))
while True:
	user_input = input("Enter an expression (or 'q' to quit): ")
	s.send(user_input.encode('utf-8'))
# read a response
	response = s.recv(1024)
	print("CLIENT RECEIVED: ",response.decode())

# close the connection
s.close()
