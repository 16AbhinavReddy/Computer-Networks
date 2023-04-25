# Simulation Testbench
#
# Author: Neha Karanjkar


import simpy
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Applications import SendingApplication,ReceivingApplication
from Channel import UnreliableChannel
from Protocol_rdt2 import *
L1=[]
L2=[]
# Create a simulation environment


L=[]
j=0
i=0
while 0<=j<=0.9:
	env=simpy.Environment()
	# Populate the simulation environment with objects:
	sending_app	  = SendingApplication(env)
	receiving_app = ReceivingApplication(env)
	rdt_sender	  = rdt_Sender(env)
	rdt_receiver  = rdt_Receiver(env)
	channel_for_data  = UnreliableChannel(env=env,Pc=j,Pl=0,delay=2,name="DATA_CHANNEL")
	channel_for_ack	  = UnreliableChannel(env=env,Pc=0,Pl=0,delay=2,name="ACK_CHANNEL")

	# connect the objects together
	# .....forward path...
	sending_app.rdt_sender = rdt_sender
	rdt_sender.channel = channel_for_data
	channel_for_data.receiver = rdt_receiver
	rdt_receiver.receiving_app = receiving_app
	# ....backward path...for acks
	rdt_receiver.channel = channel_for_ack
	channel_for_ack.receiver = rdt_sender
	L2.append(j)
	# Run simulation'for 
	while rdt_receiver.receiving_app.total_packets_received<100:
		env.run(until=i+1)
		i = i+1
		
		L.append(rdt_sender.rtt)
	L1.append(np.array(L).mean())
	j = j+0.001
print(L1)
print(L2)
sns.lineplot(x=L2,y=L1)
plt.show()



