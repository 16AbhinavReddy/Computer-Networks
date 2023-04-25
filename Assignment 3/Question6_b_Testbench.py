# Simulation Testbench
#
# Author: Neha Karanjkar


import simpy
from Applications import SendingApplication,ReceivingApplication
from Channel import UnreliableChannel
from Protocol_rdt2 import *

# Create a simulation environment
env=simpy.Environment()

# Populate the simulation environment with objects:
sending_app	  = SendingApplication(env)
receiving_app = ReceivingApplication(env)
rdt_sender	  = rdt_Sender(env)
rdt_receiver  = rdt_Receiver(env)
delayone = 2
channel_for_data  = UnreliableChannel(env=env,Pc=0.1,Pl=0.2,delay=delayone,name="DATA_CHANNEL")
channel_for_ack	  = UnreliableChannel(env=env,Pc=0.3,Pl=0.3,delay=delayone,name="ACK_CHANNEL")

rdt_sender.timeout_value = 3*delayone

# connect the objects together
# .....forward path...
sending_app.rdt_sender = rdt_sender
rdt_sender.channel = channel_for_data
channel_for_data.receiver = rdt_receiver
rdt_receiver.receiving_app = receiving_app
# ....backward path...for acks
rdt_receiver.channel = channel_for_ack
channel_for_ack.receiver = rdt_sender

# Run simulation
env.run(until=1000)


