# This is the client program that uses UDP

# Sequence:
#
# 1. Create a socket
# 2. Send messages to it
# (We need to know the server's hostname and port.)

import socket
import time, random

# create a socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# The first argument should be AF_INET
	# The second argument is SOCK_STREAM for TCP service
	#    and SOCK_DGRAM for UDP service\
listone=["SEND_DATE","SEND_DATE","SEND_DATE","SEND_TIME","SEND_TIME","SEND_TIME","q"]
while True:
    
    host='10.196.15.27'
    port=43387  # this is the server's port number, which the client needs to know

	# send some bytes (encode the string into Bytes first)
    message = random.choice(listone)
    s.sendto( message.encode('utf-8'), (host,port))


	# see if the other side responds
    data, addr = s.recvfrom(1024)
    print("Client received MESSAGE=",data.decode()," from ADDR=",addr)
    time.sleep(random.uniform(1,2))
    
	
	
	 # buffer size is 1024 bytes


# close the connection

