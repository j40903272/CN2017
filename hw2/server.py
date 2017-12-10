import socket
import func
import time

address = func.load_config()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
recvmsg = []

print ("start listening")
try:
	while True:
		recvdata, (remotehost, remoteport) = s.recvfrom(1024)
		print ("[%s:%s] connect" % (remotehost, remoteport))

		if not recvdata:
			print ("client closed")
			break

		print ("received data from", remotehost, remoteport)
		print (recvdata)
		recvmsg.append(recvdata)
		senddataLen = s.sendto("recieved!".encode('utf-8'), (remotehost, remoteport))
		print ("send data len", senddataLen)
except:
	s.close()

	cnt = 0
	num = 0
	for i in recvmsg:
		i = int(i.decode('utf-8'))
		if i != cnt:
			print ("out of order", i, cnt)
			num += 1
		cnt += 1
	print (num)