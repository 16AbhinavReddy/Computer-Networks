# SimPy model for the Reliable Data Transport (rdt) Protocol 2.0 (Using ACK and NAK)

#
# Sender-side (rdt_Sender)
#	- receives messages to be delivered from the upper layer 
#	  (SendingApplication) 
#	- Implements the protocol for reliable transport
#	 using the udt_send() function provided by an unreliable channel.
#
# Receiver-side (rdt_Receiver)
#	- receives packets from the unrealible channel via calls to its
#	rdt_rcv() function.
#	- implements the receiver-side protocol and delivers the collected
#	data to the receiving application.

# Author: Neha Karanjkar


import simpy
import random
from Packet import Packet
import sys

# the sender can be in one of these two states:
WAITING_FOR_CALL_0_FROM_ABOVE =0
WAIT_FOR_ACK_0=1
WAIT_FOR_ACK_1=2
WAITING_FOR_CALL_1_FROM_ABOVE =3



class rdt_Sender(object):

	def __init__(self,env):
	
		self.timeout_value = 10
		self.timer_is_running = False
		self.timer = None
		# Initialize variables
		self.env=env 
		self.channel=None
		
		# some state variables
		self.state = WAITING_FOR_CALL_0_FROM_ABOVE
		self.seq_num=0
		self.packet_to_be_sent=None
	def timer_behavior(self):
		try:
			self.timer_is_running=True
			yield self.env.timeout(self.timeout_value)
			self.timer_is_running=False
			self.timeout_action()
		except simpy.Interrupt:
			self.timer_is_running=False
	def start_timer(self):
		if (self.timer_is_running==False):
			self.timer = self.env.process(self.timer_behavior())
	def stop_timer(self):
		if (self.timer_is_running==True):
			self.timer.interrupt()
	def timeout_action(self):
		self.stop_timer()
		self.channel.udt_send(self.packet_to_be_sent)
		self.start_timer()
	def rdt_send(self,msg):

		if self.state==WAITING_FOR_CALL_0_FROM_ABOVE:
			# This function is called by the 
			# sending application.
			
			# create a packet, and save a copy of this packet
			# for retransmission, if needed
			self.packet_to_be_sent = Packet(seq_num=self.seq_num, payload=msg)
			self.seq_num+=1
			self.seq_num =self.seq_num%2
			# send it over the channel
			self.channel.udt_send(self.packet_to_be_sent)
			self.start_timer()
			# wait for an ACK or NAK
			self.state=WAIT_FOR_ACK_0
			return True
		elif self.state==WAITING_FOR_CALL_1_FROM_ABOVE:
			# This function is called by the 
			# sending application.
			
			# create a packet, and save a copy of this packet
			# for retransmission, if needed
			self.packet_to_be_sent = Packet(seq_num=self.seq_num, payload=msg)
			self.seq_num+=1
			self.seq_num =self.seq_num%2
			# send it over the channel
			self.channel.udt_send(self.packet_to_be_sent)
			self.start_timer()
			# wait for an ACK or NAK
			self.state=WAIT_FOR_ACK_1
			return True
			
		else:
			return False
	
	def rdt_rcv(self,packt):
		# This function is called by the lower-layer 
		# when an ACK/NAK packet arrives
		if self.state==WAIT_FOR_ACK_0:
			if (packt.corrupted or packt.seq_num==1):
				self.channel.udt_send(self.packet_to_be_sent)
			else:
				if (packt.payload=="ACK"):
					self.state=WAITING_FOR_CALL_1_FROM_ABOVE
					self.stop_timer()
				
		
		elif self.state==WAIT_FOR_ACK_1:
			if (packt.corrupted or packt.seq_num==0):
				self.channel.udt_send(self.packet_to_be_sent)
			else:
				if (packt.payload=="ACK"):
					self.state=WAITING_FOR_CALL_0_FROM_ABOVE
					self.stop_timer()

WAITING_FOR_CALL_0_FROM_BELOW =0	
WAITING_FOR_CALL_1_FROM_BELOW =1

class rdt_Receiver(object):
	def __init__(self,env):
		# Initialize variables
		self.env=env 
		self.receiving_app=None
		self.channel=None
		self.state = WAITING_FOR_CALL_0_FROM_BELOW
		

	def rdt_rcv(self,packt):
		# This function is called by the lower-layer when a packet arrives
		# at the receiver
		
		# check whether the packet is corrupted
		
		if (self.state==WAITING_FOR_CALL_0_FROM_BELOW):
			if (packt.corrupted or packt.seq_num==1):
				response = Packet(seq_num=1, payload="ACK")
				self.channel.udt_send(response)
			else:
				response = Packet(seq_num=0, payload="ACK")
				self.channel.udt_send(response)
				self.receiving_app.deliver_data(packt.payload)
				self.state = WAITING_FOR_CALL_1_FROM_BELOW
				
			
		else:
			if (packt.corrupted or packt.seq_num==0):
				#print("hello")
				response = Packet(seq_num=0, payload="ACK")
				self.channel.udt_send(response)
			else:
				#print("hello1")
				response = Packet(seq_num=1, payload="ACK")
				self.channel.udt_send(response)
				self.receiving_app.deliver_data(packt.payload)
				self.state = WAITING_FOR_CALL_0_FROM_BELOW
				
		
		
		
		
		
		
		
		

