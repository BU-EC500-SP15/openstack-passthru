import os
import socket
from swiftclient import client
#from flask import Flask, request, redirect, url_for,send_from_directory
#from werkzeug import secure_filename
usr = 'admin'
key = 'open'
authurl = 'http://10.0.2.15:35357/v2.0'
ten = 'admin'

container_name = 'my-new-container'

def connect_swift():			###for createing connection to the account and getting an object to work on swift.
	con = client.Connection(authurl=authurl,user=usr, key=key,auth_version='2',tenant_name= 'admin', retries=5,)
	return con
	
def create_container(con):	###for creating a container from the connection object.
	try:
		con.put_container('a1')
	except:
		print 'error'
		return
	else:
		print 'OK'
		return
def delete_container(con):	### for deleting a container from the connection object.
	try:
		con.delete_container('a1')
	except:
		print 'error'
		return
	else:
		print 'OK'
		return

if __name__ == '__main__':
	
	s = socket.socket()
	host = socket.gethostname()
	port = 5002
	s.bind((host,port))		##binding port and host to socket.
	s.listen(5)			###waiting for the client connection.
	c, addr = s.accept()		###accepting the client connection.
	st =  ''
	c.send('Welcome to test_server:\n')	
	c.send('>>>')
	conn = connect_swift()		###getting a connection object.
	while (True):
		
		print 'Got connection from ',addr
		st = c.recv(1024)
		print st
		if st =='exit':
			break
		elif st == 'post':
			create_container(conn)
		elif st == 'delete':
			delete_container(conn)
			
		#print 'send ....'
		#c.send('>>>')
		
	conn.close()		###closing the swift connection.
	c.close()		###closing the client connection.

