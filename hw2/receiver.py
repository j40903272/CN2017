import socket
import func
import time
import sys

server_addr = func.load_config()
filepath = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print (s.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF))
bufsize = 8192

print ("receiver start")
msg = "[LOGIN]:[R]"
# login
while True:
	if not s.sendto(msg.encode('utf-8'), server_addr):
		print ("send failed")
	
	recvdata, (remotehost, remoteport) = s.recvfrom(bufsize)
	#print ("recieved", recvdata)
	if not recvdata:
		print ("server closed")
		exit()
	elif recvdata == "[OK]".encode('utf-8'):
		print ("login success")
		break
	



# wait to recieve data
while True:
	recvdata, (remotehost, remoteport) = s.recvfrom(bufsize)
	#print ("recieved", recvdata)
	if recvdata == "[START]".encode('utf-8'):
		break


cnt = 0
size = 0
filedata = b''
s.settimeout(10)
print ("start recieving...")
try:
	recvdata, (remotehost, remoteport) = s.recvfrom(bufsize, socket.MSG_TRUNC)
	print ("recieved", len(recvdata), recvdata)
	while len(recvdata) <= 1024:

		if (remotehost, remoteport) != server_addr:
			print (server_addr, remotehost, remoteport)
			print ("unknown host ", remotehost, remoteport, recvdata)

		head, body = func.parse(recvdata)
		
		if size == 32:
			print ("drop\tdata\t#%d" % head)
			f.write(filedata)
			filedata = b''
			size = 0
			print ("flush")
			continue
		
		if head == cnt:
			print ("recv\tdata\t#%d" % head)
			if cnt == 0:
				filepath += body.decode('utf-8')
				f = open(filepath, "wb")
			else:
				filedata += body
				size += 1
			cnt += 1
		else:
			print ("drop\tdata\t#%d" % head)
			

		if not s.sendto(str(cnt-1).encode('utf-8'), server_addr):
			print ("send failed")
		else:
			print ("send\tack\t#%d" % (cnt-1))
		
		recvdata, (remotehost, remoteport) = s.recvfrom(bufsize, socket.MSG_TRUNC)
		#print ("#######", len(filedata), cnt)

except socket.timeout:
	print ("timeout")

print ("recv\tfin")
print ("send\tfinack")
f.write(filedata)
print ("flush")
f.close()
s.sendto("[OK]".encode('utf-8'), server_addr)
s.close()