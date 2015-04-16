'''
Project name : checkpointing
Created on : Wed Apr  8 16:48:07 2015
Author : Anant Pushkar
DS term Project
'''
import sys
debug_mode = len(sys.argv)>1 and sys.argv[1]=="DEBUG"
def debug(msg):
	if debug_mode:
		print msg

import time
from application import Application 

base_port = 5100
syslist = [
	{
	"name" : "tango"   , 
	"ip"   : "10.132.239.80" , 
	"port" : base_port
	},
	{
	"name" : "charlie" , 
	"ip"   : "10.102.66.128" , 
	"port" : base_port
	}
]

app1 = Application(config = {
		"TCP_IP"   : "127.0.0.1",
		"TCP_PORT" :  str(base_port)    , 
		"peers"    : syslist    ,
		"name"     : "tango"
	})
'''
app2 = Application(config = {
		"TCP_IP"   : "127.0.0.1",
		"TCP_PORT" :  str(base_port+50)    , 
		"peers"    : syslist    ,
		"name"     : "charlie"
	})
'''
app1.start_session()
#app2.start_session()

time.sleep(2)

app1.start_transactions()
#app2.start_transactions()