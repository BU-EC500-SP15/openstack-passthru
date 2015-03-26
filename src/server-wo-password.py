import os
import socket
from swiftclient import client
usr = 'singh1'
key = 'JRARJNS'
authurl = 'http://140.247.152.207:35357/v2.0'
ten = 'EC500-openstack-passthru'


def connect_swift():			###for createing connection to the account and getting an object to work on swift.
	con = client.Connection(authurl=authurl,user=usr, key=key,auth_version='2',tenant_name=ten, retries=10,)
	return con

from swiftclient import ClientException

def create_container(con, container):	###for creating a container from the connection object.
	try:
		con.put_container(container)
	except ClientException as e:
                return e.msg, e.http_status
	else:

		return "", 204
def delete_container(con, container):	### for deleting a container from the connection object.
	try:
		con.delete_container(container)
	except ClientException as e:
		return e.msg, e.http_status
	else:
                return "", 204
def get_container(con, container): ### for listing a container's objects and information.
	try:
		headers, result = con.get_container(container)
		return str(result),200
	except ClientException as e:
		return e.msg, e.http_status
	else:
		return "", 204

def get_account(con):
	try:
		headers, result = con.get_account()
		#print "wetwerewr"
		#print result
		#print type(result)
		return str(headers), 200
		#return str(result),200
	except ClientException as e:
		print e.msg		
		return e.msg, e.http_status
	else:
		"", 204
def get_object(con,container,obj):  ### for download an object from the container
        try:
		
                headers,result = con.get_object(container, obj)
		return str(result),200
        except ClientException as e:
		
                return e.msg, e.http_status
        else:
		
                return "object find", 204

################### Update contaner, object, and account require testing                
def update_containerMetaData(con, container): ###update container metadata 
	try:
		con.post_container(container)
	except ClientException as e:
                return e.msg, e.http_status
	else:
		return "", 204

def update_objectMetaData(con, container, obj): ###update objects metadata
	try:
		con.post_object(container, obj)
	except ClientException as e:
                return e.msg, e.http_status
	else:
		return "", 204
			
def update_accountMetaData(con): ###update objects metadata- Not sure if its implemented properly
	try:
		con.post_account()
	except ClientException as e:
                return e.msg, e.http_status
	else:
		return "", 204
			

def upload_object(con, container,obj,objct):		###method to upload the objects in container.	
	try:
		ret = con.put_object(container, obj,objct)
	except ClientException as e:

		return e.msg, e.http_status
	else:

                return "", 204

def delete_object(con,container,obj):			###method to delete the objects in container.
	try:
		con.delete_object(container, obj)
	except ClientException as e:

		return e.msg, e.http_status
	else:

                return "", 204
              
def head_account(con):### show account metadata
                try:
			headers=con.head_account()
			##print headers
			return str(headers),200
		except ClientException as e:
			print e.msg
			return e.msg,e.http_status
		else:
			return "",204

def head_container(con,container):### show container metadata
                try:
			headers=con.head_container(container)
			##print headers
			return str(headers),200
		except ClientException as e:
			return e.msg,e.http_status
		else:
			return "",204
def head_object(con,container,obj):### show object metadata
                try:
			headers=con.head_object(container,obj)
			return headers,200
		except ClientException as e:
			return e.msg,e.http_status
		else:
			return "",204

##################################################################################################### flask:

from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST', 'HEAD'])
def func1():
	if request.method == 'GET':
		con = connect_swift()
		return get_account(con)
	elif request.method == 'POST':
		con = connect_swift()
		return update_accountMetaData(con)
	elif request.method=='Head':
 		con=connect_swift()
		head =  head_account(con)
		print head
		return head
	
	else:
		return "Not yet implemented", 501

@app.route("/<container>", methods=['PUT', 'DELETE', 'GET', 'POST', 'HEAD'])
def func2(container):
        if request.method == 'PUT':
                con = connect_swift()
                return create_container(con, container)
        elif request.method == 'DELETE':
                con = connect_swift()
                return delete_container(con, container)
	elif request.method == 'GET':
		con = connect_swift()
		return get_container(con, container)
	
	elif request.method=='HEAD':
		con=connect_swift()
		return head_container(con,container)
        else:
                return "Not yet implemented", 501


@app.route("/<container>/<obj>", methods=[ 'PUT', 'DELETE', 'GET', 'POST', 'HEAD', 'COPY'])
def func3(container, obj):
        if request.method=='GET':
		
                con=connect_swift()
                return get_object(con,container,obj)
	elif request.method == 'PUT':				###method to upload/replace the objects in container.
		con = connect_swift()
		objct = request.get_data()
		return upload_object(con,container,obj,objct)
	elif request.method == 'DELETE':			###method to delete an object from a container.
		con = connect_swift()
		return delete_object(con,container,obj)
	elif request.method == 'COPY':   ###method to copy an object
		
		con = connect_swift()
		p=request.headers.get('Destination')
		p1=str(p).split('/')
		#print p1
		header,result = con.get_object(container,obj)
		return upload_object(con,p1[1],p1[2],result)
	elif request.method=='HEAD':
		con=connect_swift()
		return get_object(con,container,obj)
	

        else:
        	return "Not Yet Implemented", 501

	




if __name__ == "__main__":
        app.run()
