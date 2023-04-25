import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("10.196.12.43", 5000))
contin = True
def handle_input(client):
    
    global contin
    while contin:
        #message = client.recv(1024).decode("utf8")
        #print(message)
        message = input(">>")
        if message=="quit":
        	contin=False
        	
        	
        
        client.send(message.encode("utf8"))
def handle_output(client):
    
    global contin
    while contin:
        message = client.recv(1024).decode("utf8")
        print(message)
        #message = input(">>")
        #if message=="quit":
        	#contin=False
        	
        
        #client.send(message.encode("utf8"))

name = input("Enter Your Name:")
client.send(name.encode("utf8"))




#while contin:
    
    
    #print(message)
    #if contin==True:
	    
input_thread = threading.Thread(target=handle_input, args=(client,))
output_thread = threading.Thread(target = handle_output, args=(client,))
input_thread.start()
output_thread.start()
    
    

    	
	    


