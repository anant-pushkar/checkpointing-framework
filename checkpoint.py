import abc
import sys
import json
from node import Node
import time
import threading
import os

DEBUG = True
DELTA = 2000
INTRA_CP_TIME = 10000

class Checkpoint(Node):
	
	__metaclass__ = abc.ABCMeta
	
	def __init__(self,config):
		Node.__init__(self , config)
		self.previous_cp_time = -1

		if self.name + ".log" in os.listdir("."):
			self.recover()

		self.regulator = threading.Thread(target=self.regulate_cp , args=())
		self.regulator.start()

	def recover(self):
		if DEBUG : print self.name , " Making recovery"

		log = open(self.name + ".log")
		state = log.read()
		log.close()

		self.init_state(state)

		log = open(self.name + ".msg")
		lines = log.read().splitlines()
		for line in lines:
			line = line.split()
			if len(line)==0:
				break
			if line[0] == "SEND":
				self.send_handler(" ".join(line[1:]))
			elif line[0] == "RECV":
				self.receive_handler(" ".join(line[1:]))
			elif line[0] == "SENDFAIL":
				self.sendfail_handler(" ".join(line[1:]))
		log.close()

		log = open(self.name + ".msg" , "w")
		log.close()

		print self.name , "After recovery state :" , self.get_state()

	def send_fail(self , msg):
		log = open(self.name + ".msg" , "a+")
		log.write("SENDFAIL " + msg + "\n")
		log.close()

	def regulate_cp(self):
		while True:
			self.take_cp(self.get_state())
			time.sleep(INTRA_CP_TIME/1000)

	def take_cp(self , state):
		state = self.get_state()
		if DEBUG : print self.name , " # Taking CP :" , state

		log = open(self.name + ".log" , "w")
		log.write(state + "\n")
		log.close()

		log = open(self.name + ".msg" , "w")
		log.close()

		self.previous_cp_time = time.time()

	def send(self , ip , port , msg , seq=None , identifier=None):
		if DEBUG: print self.name , " # Sending :" , msg , " to " , (ip,port)
		now = time.time()
		while self.previous_cp_time + INTRA_CP_TIME - DELTA <= now:
			time.sleep(DELTA)
			now = time.time()

		log = open(self.name + ".msg" , "a+")
		log.write("SEND " + msg + "\n")
		log.close()

		Node.send(self , ip , port , msg , seq , identifier)

	def on_receive(self , msg , peer , addr):
		if DEBUG: print self.name , " # received :" , msg , " from " , (peer,addr)
		log = open(self.name + ".msg" , "a+")
		log.write("RECV " + msg + "\n")
		log.close()

		self.receive_handler(msg)

	def init(self , arg=None):
		pass

	@abc.abstractmethod
	def init_state(self , state):
		pass

	@abc.abstractmethod
	def send_handler(self , msg):
		pass

	@abc.abstractmethod
	def sendfail_handler(self , msg):
		pass

	@abc.abstractmethod
	def receive_handler(self , msg):
		pass

	@abc.abstractmethod
	def get_state(self):
		pass