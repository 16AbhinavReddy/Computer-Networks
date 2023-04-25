# This is the Server program
#
# Sequence of steps:
#	1. create a "welcome" socket for listening to new connections 
#	2. bind the socket to a host and port
#	3. start listening on this socket for new connections
#	4. accept an incoming connection from the client
#   5. send and receive data over the "connection" socket


import socket

def perform_operation(operator, operand1, operand2):
    if operator == '+':
        return operand1 + operand2
    elif operator == '-':
        return operand1 - operand2
    elif operator == '*':
        return operand1 * operand2
    elif operator == '/':
        return operand1 / operand2
    else:
        return "Invalid operator"

#  create a socket for listening to new connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				# use SOCK_STREAM for TCP
				# use SOCK_DGRAM for UDP

# bind it to a host and a port
host = '10.196.15.27'
port = 43389  # arbitrarily chosen non-privileged port number
s.bind((host,port))
print("Server started...waiting for a connection from the client")

# start listening for TCP connections made to this socket
# the argument "1" is the max number of queued up clients allowed
s.listen(1) 

# accept a connection
connection_socket, addr = s.accept()
print("Connection initiated from ",addr)

# receive some bytes and print them
# the argument 1024 is the maximum number of characters to be read at a time
data = connection_socket.recv(1024)
print("SERVER RECEIVED: ", data.decode())

# send some bytes...
# connection_socket.send("Whose there?".encode('utf-8'))
while True:
    request = connection_socket.recv(1024).decode()
    if request == 'q':
        print("Session ended")
        break
    print(f"Received request: {request}")
    try:
        operand1, operator, operand2 = request.split()
        operand1 = float(operand1)
        operand2 = float(operand2)
        result = perform_operation(operator, operand1, operand2)
        response = str(result)
    except:
        response = "Invalid expression"
    connection_socket.sendall(response.encode())


# close the connection
connection_socket.close()
s.close()
