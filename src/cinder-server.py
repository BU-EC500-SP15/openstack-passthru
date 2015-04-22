import os
import pdb#;pdb.set_trace()
import socket
#pdb.set_trace()
from cinderclient import client
import json



#cinderurl= 'http://10.31.27.207:8776/v2/d5785e4393ba4db5871c34b6a6c3ef7b'

version='2'
uname='estherlu'
pwd='31415926'
ten = 'EC500-openstack-passthru'
authurl = 'http://140.247.152.207:35357/v2.0'



def connect_cinder(): #########works
	con=client.Client(version, uname, pwd , ten, authurl)
	return con


from cinderclient import exceptions


#####list volumes with name and size
def get_volumes(con):
	try:                              
		vlist=con.volumes.list()
#		print vlist[1]
#		print vlist[0]
		volumes=[]
		for i in range(len(vlist)):
			vdict=vlist[i].__dict__
			vol=[]
			vol.append(vdict['id'].encode('ascii','ignore'))
			vol.append(vdict['name'].encode('ascii','ignore'))
			vol.append(vdict['size'])
			print vol
			volumes.append(vol)
		return str(volumes),200
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204


######list volumes with whole detail
def get_volumes_detail(con):
	try:  
		vlist=con.volumes.list()
		dvols=[]
		for i in range(len(vlist)):
			vdict=vlist[i].__dict__
			dvols.append(vdict)
		return str(dvols)
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204


#####create volume
def create_volume(con,name1,size1):
	try:
		p=str(con.volumes.create(size1,name=name1))
		return p,200
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204


#####get a volume's whole detail by its uuid
def get_a_volume(con,volumeid):
	try:
		vid=unicode(volumeid)
		vol=con.volumes.get(vid)
		voldict=vol.__dict__
		return str(voldict),200
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204


#####delete a volume by its uuid
def delete_volume(con,volumeid):
	try:
		vid=unicode(volumeid)
		vol=con.volumes.get(vid)
		con.volumes.delete(vol)
		return "",200
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204

#####increase the size of a volume
def extend_volume(con,volumeid,size):
	try:
		vid=unicode(volumeid)
		vol=con.volumes.get(vid)
		con.volumes.extend(vol,size)
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204
          


			
##################################################################################################### flask:

from flask import Flask, request
app = Flask(__name__)


@app.route("/v2/<tenid>/volumes", methods=[ 'GET', 'POST'])
def func1(tenid): 
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/volumes
#####POST: curl -X POST http://localhost:5003/v2/EC500-openstack-passthru/volumes -H "Volume-Name:test3" -H "Volume-Size:1"		        
        if  request.method == 'GET':		
		con=connect_cinder()
		return get_volumes(con)
	elif request.method == "POST":
		con=connect_cinder()
		name=request.headers.get('Volume-Name').encode('ascii','ignore')
		size=int(request.headers.get('Volume-Size'))
		print type(name)
		return 	create_volume(con,name,size)
        else:
                return "No Such Function", 501



@app.route("/v2/<tenid>/volumes/detail", methods=[ 'GET'])
def func2(tenid): 
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/volumes/detail
	if request.method == 'GET':
		con=connect_cinder()
		return get_volumes_detail(con)
	else:
		return "No Such Function", 501



@app.route("/v2/<tenid>/volumes/<vid>", methods=[ 'GET', 'PUT', 'DELETE'])
def func3(tenid,vid): 
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/volumes/uuid
#####DELETE: curl -X DELETE http://localhost:5003/v2/EC500-openstack-passthru/volumes/uuid
	if request.method == 'GET':
		con=connect_cinder()
		return get_a_volume(con,vid)
	elif request.method == 'PUT':###to be implemented
		con=connect_cinder()
		return 'not yet'
	elif request.method == 'DELETE':
		con=connect_cinder()
		return delete_volume(con,vid)
	else:
		return "No Such Function", 501
	

@app.route("/v2/<tenid>/volumes/<vid>/action", methods=[ 'POST'])
def finc4(tenid,vid):
	if request.method == 'POST':
		con=connect_cinder()
		size=int(request.headers.get('Volume-Size'))
		return extend_volume(con,vid,size);
	else:
		return "No Such Function", 501




if __name__ == "__main__":
        app.run(None,5003,True)
