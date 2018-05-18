import redis
dir(redis)
from mongo_connect import connectMongo
import pymongo
import json
import pprint

r = redis.Redis()
collection = connectMongo()

subscribing = False;
topic = "";
msg_board="";
while True:
	try:
		if subscribing:
			print("Sub")
			for item in p.listen():	
				print(item)

		cmd = raw_input('Enter your command: ')
		print(cmd)
		cmd_parts = cmd.split(" ")
		print(cmd_parts)

		if cmd_parts[0] == "select":
			if(len(cmd_parts)!=2):
				print "ERROR: incorrect format. Correct format is: select <board_name>"
				continue
			msg_board = cmd_parts[1]
		elif cmd_parts[0] == "read":
			if(len(cmd_parts)!=1):
				print "ERROR: incorrect format. Correct format is: read"
				continue
			if(len(msg_board)==0):
				print "ERROR: no board is selected"
				continue
			else:
				RQ0 = collection.find({"NameOfMessageBoard":msg_board})
				for data in RQ0:
					pprint.pprint(data)
		elif cmd_parts[0] == "write":
			if(len(cmd_parts)<2):
				print "ERROR: incorrect format. Correct format is: write <message>"
				continue
			if(len(msg_board)==0):
				print "ERROR: no board is selected"
			else:
				to_pub = ' '.join(cmd_parts[1:])
				res = r.publish(msg_board, to_pub)
				print res
				collection.insert({"NameOfMessageBoard":msg_board, "Message":to_pub})
		elif cmd_parts[0] == "listen":
			if(len(cmd_parts)!=1):
				print "ERROR: incorrect format. Correct format is: listen"
				continue
			if(len(msg_board)==0):
				print "ERROR: no board is selected"
				continue
			else:
				subscribing = True;
				p = r.pubsub()
				res = p.subscribe(msg_board)
				print res
		elif cmd_parts[0] == "stop":
			if(len(cmd_parts)!=1):
				print "ERROR: incorrect format. Correct format is: stop"
				continue
			if(len(msg_board)==0):
				print "ERROR: no board is selected"
				continue
			if(subscribing == False):
				print "ERROR: not listening"
				continue
			subscribing = False
			break
		elif cmd_parts[0] == "quit":
			break;
		else:
			print("Input format wrong");

	except KeyboardInterrupt:
		print
		subscribing = False