import socket
import func
import time
import sys

server_addr = func.load_config()
filepath = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
extend = "." + filepath.split(".")[-1]
fail = 0

print ("sender start")
msg = "[LOGIN]:[S]"
# login
while True:
	if not s.sendto(msg.encode('utf-8'), server_addr):
		print ("send failed")

	s.settimeout(1)
	try:
		recvdata, (remotehost, remoteport) = s.recvfrom(1024)
		print ("recieved", recvdata)
		if not recvdata:
			print ("server closed")
			exit()
		elif recvdata == "[OK]".encode('utf-8'):
			print ("login success")
			break
	except:
		continue

# wait for server to start transfer
s.settimeout(None)
while True:
	recvdata, (remotehost, remoteport) = s.recvfrom(1024)
	if recvdata == "[START]".encode('utf-8'):
		print ("start sending...")
		break


cnt = 0
maxcnt = 0
window = 1
threshold = 16
headersize = 10
payload = 1024-headersize
s.settimeout(1)
f = open(filepath, "rb")
data = extend.encode('utf-8')
# send file
while True:
	offset = cnt
	for i in range(1, window+1):
		data = func.concat(cnt, data)
		if s.sendto(data, server_addr):
			if cnt > maxcnt:
				print ("send\tdata\t#%d,\twinsize = %d" % (cnt, window))
			else:
				print ("resnd\tdata\t#%d,\twinsize = %d" % (cnt, window))
		else:
			print ("send failed")
		cnt += 1
		data = f.read(payload)
		if not data:
			break

	maxcnt = max(cnt, maxcnt)
	x = cnt - offset
	cnt = offset
	recvack = []
	for i in range(1, x+1):
		try:
			recvdata, (remotehost, remoteport) = s.recvfrom(1024)
			recvdata = recvdata.decode()
			recvack.append(int(recvdata))
			print ("recv\tack\t#%d" % int(recvdata))

		except socket.timeout:
			break


	if len(recvack) < x:
		for i in sorted(recvack):
			if i == cnt:
				cnt += 1
			else:
				break

		threshold = max(window/2, 1)
		print ("time\tout\t\tthreshold = %d" % threshold)
		window = 1
		f.seek((cnt-1)*payload,0)
		data = f.read(payload)
	else:
		if not data:
			break
		cnt += window
		if window < threshold:
			window *= 2
		else:
			window += 1


while True:
	if not s.sendto(("fin").encode('utf-8'), server_addr):
		print ("send failed")
	else:
		print ("send\tfin")
	try:
		recvdata, (remotehost, remoteport) = s.recvfrom(1024)
		if recvdata.decode('utf-8') == "[OK]":
			print ("recv\tfinack")
			break
	except socket.timeout:
		continue



f.close()
s.close()