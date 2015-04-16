
import json
import random
import threading
from checkpoint import Checkpoint
from node import Node
import time
import signal

LOG_FILENAME = "transactions.log"
TRANSACTION_INTERVAL = 5
CHECKPOINT_INTERVAL  = 20
INIT_ACC = 10000
INTRA_TRANSACTION_TIME = 2

class Application(Checkpoint):
	
	def __init__(self , config ):
		self.acc = INIT_ACC
		Checkpoint.__init__(self,config)
		self.buff = 0

	def log_pending(self):
		self.send_fail(self.buff)

	def start_transactions(self):
		signal.signal(signal.SIGINT , self.log_pending)
		signal.signal(signal.SIGILL , self.log_pending)
		signal.signal(signal.SIGTERM , self.log_pending)
		signal.signal(signal.SIGSEGV , self.log_pending)
		signal.signal(signal.SIGABRT , self.log_pending)
		signal.signal(signal.SIGFPE , self.log_pending)
		while True:
			peer = random.choice(self.peers)
			if peer["name"]!=self.name:
				break
		amt  = random.randint(1 , self.acc/100)
		self.buff += amt
		try:
			self.send_handler(amt)
			self.send(peer["ip"] , peer["port"] , str(amt))
			time.sleep(INTRA_TRANSACTION_TIME)
		except:
			print self.name , "## Could not send msg to "  , peer["name"]
			self.send_fail(str(amt))

		self.buff -= amt

	def get_state(self):
		return str(self.acc)

	def send_handler(self , amt):
		self.acc -= int(amt)

	def sendfail_handler(self , amt):
		self.acc += int(amt)

	def receive_handler(self , msg):
		self.acc += int(msg)

	def init_state(self , state):
		self.acc = int(state)
		
		
