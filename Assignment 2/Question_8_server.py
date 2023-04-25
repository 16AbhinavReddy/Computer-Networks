import socket
import threading
import time

def broadcast(message, client):
    for c in clients:
        if c != client:
            c.send(message)

def handle(client):
    if client not in clients:
	    print("{} has connected".format(address))
	    
	    name = client.recv(1024).decode("utf8")
	    broadcast("{} has joined the chat.".format(name).encode("utf8"), client)
	    clients.append(client)
    while True:
        message = client.recv(1024).decode("utf8")
        if message == "quit":
            client.close()
            clients.remove(client)
            broadcast("{} has left the chat.".format(name).encode("utf8"), client)
            print("{} has left the chat.".format(name).encode("utf8"), client)
            break
        broadcast("{}: {}".format(name, message).encode("utf8"), client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("10.196.12.43", 5000))
server.listen()

clients = []

print("Chat server started on port 5000")

while True:
    client, address = server.accept()
    client_thread = threading.Thread(target=handle, args=(client,))
    client_thread.start()
