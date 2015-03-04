import socket

s= socket.socket()
host = socket.gethostname()
port = 5002
s.connect((host,port))
print s.recv(1024)
st = ''
while(True):
	st = raw_input()
	s.send(st)
	if (st == 'exit') :break
s.close
