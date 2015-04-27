import os
import pdb
import socket
#pdb.set_trace()
from swiftclient import client
import json
from flask import jsonify

#authurl = 'http://140.247.152.207:35357/v2.0'
#ten = 'EC500-openstack-passthru'
preauthurl_MOC1='http://140.247.152.223/swift/v1'
preauthurl_MOC2='http://140.247.152.223/swift/v1'
Backends = 2


def connect_swift(token,preauthurl):			###for createing connection to the account and getting an object to work on swift.
	con = client.Connection(preauthurl=preauthurl ,preauthtoken=token,auth_version='2', retries=10,)
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
def get_container(con, container,mark,end,limit): ### for listing a container's objects and information.
	try:
		headers, result = con.get_container(container,marker = mark,end_marker = end,limit = limit)
		return Response(json.dumps(result),mimetype='application/json'),200
	except ClientException as e:
		return e.msg, e.http_status
	else:
		return "", 204

def get_account(con,marker,end,limit):
	try:
		headers, result = con.get_account(marker = marker,limit = limit,end_marker = end)
		#print "wetwerewr"
		#print result
		#print format(result)
		return Response(json.dumps(result),mimetype='application/json'), 200
		#return str(result),200
	except ClientException as e:
		print e.msg		
		return e.msg, e.http_status
	else:
		"", 204
def get_object(con,container,obj):  ### for download an object from the container
        try:
		
                headers,result = con.get_object(container, obj)
		return json.dumps(result),200
        except ClientException as e:
		
                return e.msg, e.http_status
        else:
		
                return "object find", 204

################### Update contaner, object, and account require testing                
def update_containerMetaData(con, container,headers): ###update container metadata 
	try:
		con.post_container(container,headers)
	except ClientException as e:
                return e.msg, e.http_status
	else:
		return "", 204

def update_objectMetaData(con, container, obj,headers): ###update objects metadata
	try:
		con.post_object(container, obj,headers)
	except ClientException as e:
                return e.msg, e.http_status
	else:
		return "", 204
			
def update_accountMetaData(con,headers): ###update objects metadata- Not sure if its implemented properly
	try:
		con.post_account(headers)
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
			print headers
			return headers,200 #Response(json.dumps(headers),mimetype='application/json'),200
		except ClientException as e:
			print e.msg
			return e.msg,e.http_status
		else:
			return "",204

def head_container(con,container):### show container metadata
                try:
			headers=con.head_container(container)
			##print headers
			return headers,200 #Response(json.dumps(headers),mimetype='application/json'),200
		except ClientException as e:
			return e.msg,e.http_status
		else:
			return "",204
def head_object(con,container,obj):### show object metadata
                try:
			headers=con.head_object(container,obj)
			return headers,200 #Response(json.dumps(headers),mimetype='application/json'),200
		except :
			return "",204
def Hash(container):
	c_swift = str(container).split('-')
	if c_swift[0] == 'MOC1':
		#print 'in 1'
		return preauthurl_MOC1
	elif c_swift[0] == 'MOC2':
		#print 'in 2'
		return preauthurl_MOC2
	else:
		sm=0
		for letters in container:
			sm += ord(letters)
		index = sm%Backends
		if index == 0: 
			#print 'in 1'
			return preauthurl_MOC1
		elif index == 1:
			#print 'in 2'
			return preauthurl_MOC2
			
##################################################################################################### flask:

from flask import Flask, request,Response
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST', 'HEAD'])
def func1():
	#pdb.set_trace()
	if request.method == 'GET':
		header = request.args
		for key in header:
			print key
		token=request.headers.get('X-Auth-Token')
		marker = request.args.get('marker')
		end = request.args.get('end_marker')
		limit = request.args.get('limit')
		url =preauthurl_MOC1
				###needs to be changed
		urla=preauthurl_MOC2
		frmt = request.url
		print frmt
		con= connect_swift(token,url)
		cona=connect_swift(token,urla)
		result=(get_account(con,marker,end,limit))#+(get_account(cona))
		return result
			
	elif request.method=='HEAD':
		print 'in account HEAD'
		#pdb.set_trace()
		token=request.headers.get('X-Auth-Token');
 		url =preauthurl_MOC1				###needs to be changed
		con=connect_swift(token,url)
		#urla=preauthurl_MOC2
		#cona=connect_swift(token,urla)
		head,status =  head_account(con)
		#heada,statusa=head_account(cona)
		result={}		
		#result=head
		result['X-Account-Object-Count']=str(int(head['x-account-object-count']))#str(int(head['x-account-object-count'])+int(heada['x-account-object-count']))
		result['X-Account-Bytes-Used']=str(int(head['x-account-bytes-used']))#str(int(head['x-account-bytes-used'])+int(heada['x-account-bytes-used']))
		result['X-Account-Bytes-Used-Actual']=str(int(head['x-account-bytes-used-actual']))#str(int(head['x-account-bytes-used-actual'])+int(heada['x-account-bytes-used-actual']))
		result['X-Account-Container-Count']=str(int(head['x-account-container-count']))#str(int(head['x-account-container-count'])+int(heada['x-account-container-count']))
		print type(result)
		return "", status, result
	elif request.method == "POST":
		token=request.headers.get('X-Auth-Token');
		url =preauthurl_MOC1				###needs to be changed
		con=connect_swift(token,url)
		head = request.headers
		headers = {}
		for key in head:
			headers[key[0]] = key[1]
		
		return update_accountMetaData(con,headers)
	
	else:
		return "Not yet implemented", 501

@app.route("/<container>", methods=['PUT', 'DELETE', 'GET', 'POST', 'HEAD'])
def func2(container):
        if request.method == 'PUT':
		token=request.headers.get('X-Auth-Token');
                url = Hash(container)
		con=connect_swift(token,url)
                return create_container(con, container)
        elif request.method == 'DELETE':
		token=request.headers.get('X-Auth-Token');
                url = Hash(container)
		con=connect_swift(token,url)
                return delete_container(con, container)
	elif request.method == 'GET':
		token=request.headers.get('X-Auth-Token');
		marker = request.args.get('marker')
		end = request.args.get('end_marker')
		limit = request.args.get('limit')
		url = Hash(container)
		con=connect_swift(token,url)
		return get_container(con, container,marker,end,limit)
	elif request.method == "POST":
		token=request.headers.get('X-Auth-Token');
		url = Hash(container)
		con=connect_swift(token,url)
		head = request.headers
		headers = {}
		for key in head:
			headers[key[0]] = key[1]
		
		return update_containerMetaData(con, container,headers)
	
	elif request.method=='HEAD':
		print 'in container HEAD'
		#pdb.set_trace()
		token=request.headers.get('X-Auth-Token');
		url = Hash(container)
		con=connect_swift(token,url)
		head,status=head_container(con,container)
		return "",status,head
        else:
                return "Not yet implemented", 501


@app.route("/<container>/<obj>", methods=[ 'PUT', 'DELETE', 'GET', 'POST', 'HEAD', 'COPY'])
def func3(container, obj):
        if request.method=='GET':
		token=request.headers.get('X-Auth-Token');
		url = Hash(container)
		con=connect_swift(token,url)		
                return get_object(con,container,obj)
	elif request.method == 'PUT':	
		token=request.headers.get('X-Auth-Token');			###method to upload/replace the objects in container.
		print 'in upload put'
		#pdb.set_trace()
		frmt = request.url
		print frmt
		args = request.args
		for key in args:
			print key
		header = request.headers
		for key in header:
			print key
		url = Hash(container)
		con=connect_swift(token,url)
		objct = request.get_data()
		return upload_object(con,container,obj,objct)
	elif request.method == 'DELETE':
		token=request.headers.get('X-Auth-Token');			###method to delete an object from a container.
		url = Hash(container)
		con=connect_swift(token,url)
		return delete_object(con,container,obj)
	elif request.method == 'COPY':   ###method to copy an object
		token=request.headers.get('X-Auth-Token');
		url = Hash(container)
		con=connect_swift(token,url)
		p=request.headers.get('Destination')
		p1=str(p).split('/')
		#print p1
		header,result = con.get_object(container,obj)
		return upload_object(con,p1[0],p1[1],result)
	elif request.method=='HEAD':
		print 'in upload HEAD'
		#pdb.set_trace()
		token=request.headers.get('X-Auth-Token');
		url = Hash(container)
		frmt = request.url
		print frmt
		args = request.args
		for key in args:
			print key
		header = request.headers
		for key in header:
			print key
		con=connect_swift(token,url)
		head,status=head_object(con,container,obj)
		print type(status)
		result={}		
		#result=head
		#result['Accept-Ranges']=(head['Accept-Ranges'])
		if(status != 204):
			result['Last-Modified']=(head['last-modified'])
			result['etag']=(head['etag'])
			#result['X-Object-Meta-Mtime']=(head['x-object-meta-mtime'])
			result['Date']=(head['date'])
			print type(result)
			return "",status,result
		return "",status,head
	elif request.method == "POST":
		token = request.headers.get('X-Auth-Token')
		url = Hash(container)
		con=connect_swift(token,url)
		head = request.headers
		headers = {}
		for key in head:
			headers[key[0]] = key[1]
		
		return update_objectMetaData(con, container, obj,headers)
	

        else:
        	return "Not Yet Implemented", 501

	




if __name__ == "__main__":
        app.run(None,5001,True)
