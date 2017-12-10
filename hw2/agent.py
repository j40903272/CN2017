import socket
import func
import random
import sys

address = func.load_config()
loss_rate = float(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
send_addr, recv_addr = None, None
bufsize = 2048

print ("agent start")
# handle login
while True:
	recvdata, (remotehost, remoteport) = s.recvfrom(bufsize)
	print ("recieved", recvdata)
	if not recvdata:
		print ("client closed")
		break

	recvdata = recvdata.decode('utf-8').split(":")
	print (recvdata)
	if recvdata[0] == '[LOGIN]':
		print ("login attempt")
		if recvdata[1] == '[S]' and send_addr == None:
			print ("sender login")
			send_addr = (remotehost, remoteport)
		elif recvdata[1] == '[R]' and recv_addr == None:
			print ("reciever login")
			recv_addr = (remotehost, remoteport)
		if not s.sendto("[OK]".encode('utf-8'), (remotehost, remoteport)):
			print ("send failed")


	if send_addr != None and recv_addr != None:
		print ("both sender and reciever login!!")
		print (send_addr, recv_addr)
		if not s.sendto("[START]".encode('utf-8'), recv_addr):
			print ("send failed")
		if not s.sendto("[START]".encode('utf-8'), send_addr):
			print ("send failed")
		break
	
# handle forward
print ("start forwarding")
fwd, loss = 0, 0
while True:
	s.settimeout(10)
	try:
		recvdata, (remotehost, remoteport) = s.recvfrom(bufsize)
		#print ("recieved", recvdata)

		if (remotehost, remoteport) == send_addr:
			if len(recvdata) > 1024:
				s.sendto(recvdata, recv_addr)
				print ("get\tfin\nfwd\tfin")
			else:
				rand = random.uniform(0, 1)
				head, body = func.parse(recvdata)
				print ("get\tdata\t#%d" % head)
				fwd += 1
				if rand < loss_rate:
					loss += 1
					print ("drop\tdata\t#%d,\tloss rate = %f" % (head, loss/fwd))
					continue
				if not s.sendto(recvdata, recv_addr):
					print ("send failed")
				else:
					print ("fwd\tdata\t#%d,\tloss rate = %f" % (head, loss/fwd))
				

		elif (remotehost, remoteport) == recv_addr:
			head = recvdata.decode()
			if head == "[OK]":
				print ("get\tfinack\nfwd\tfinack")
				s.sendto(recvdata, send_addr)
				exit()
			else:
				print ("get\tack\t#%d" % int(head))
			if not s.sendto(recvdata, send_addr):
				print ("send failed")
			else:
				print ("fwd\tack\t#%d" % int(head))
		else:
			print ("weird msg from ", remotehost, remoteport)
	except socket.timeout:
		print ("connection timeout")
		s.close()
		break




