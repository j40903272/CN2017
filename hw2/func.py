header_size = 10
def load_config():
	try:
		ip, port = "", 0
		f = open("config", "r")
		for line in f:
			line = line.split(":")
			if line[0] == "ip":
				ip = line[1][:-1]
			elif line[0] == 'port':
				port = int(line[1])
		print (ip, port)
		return (ip, port)
	except:
		print ("load config error")
		exit()

def concat(head, body):
	#print (head)
	head = (head).to_bytes(header_size, byteorder='big', signed=True)
	if body == None:
		return head
	return head+body

def parse(msg):
	head = int.from_bytes(msg[:header_size], byteorder='big', signed=True)
	#print (head)
	body = msg[header_size:]

	return head, body
