import os
import socket
import swiftclient
#from flask import Flask, request, redirect, url_for,send_from_directory
#from werkzeug import secure_filename
usr = 'admin'
key = 'open'
authurl = 'http://10.0.2.15:35357/v2.0'
ten = 'admin'

container_name = 'my-new-container'

def connect_swift():
	conn = swiftclient.Connection('http://10.0.2.15:35357/v2.0','admin', 'open',auth_version='2',tenant_name= 'admin', retries=5,)
	if(conn.put_container('my-cont1')):
		conn.close()
		return 1
	else:
		conn.close()
		return 0

if __name__ == '__main__':
	
	s = socket.socket()
	host = socket.gethostname()
	port = 5002
	s.bind((host,port))
	s.listen(5)
	c, addr = s.accept()
	st =  ''
	c.send('Welcome to test_server:\n')	
	c.send('>>>')
	while (True):
		
		print 'Got connection from ',addr
		st = c.recv(1024)
		print st
		if st =='exit':
			break
		elif st == 'post':
			conn = connect_swift()
			if(conn == 1):
				print 1
			else:
				print 0
		#print 'send ....'
		#c.send('>>>')
		
		
	c.close()

