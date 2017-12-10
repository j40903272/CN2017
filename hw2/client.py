import socket
import func
import time

address = func.load_config()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cnt = 0

print ("start sending")
while True:
	sendlen = s.sendto(str(cnt).encode('utf-8'), address)
	print ("send len", sendlen)
	recvdata, (remotehost, remoteport) = s.recvfrom(1024)

	if not recvdata:
		print ("server closed")
		break

	print ("received data from", remotehost, remoteport)
	print (recvdata)
	cnt += 1

s.close()