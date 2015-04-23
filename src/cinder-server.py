import os
import socket
from cinderclient import client
from cinderclient.v2 import volume_snapshots
import json
import pdb
import copy

#cinderurl= 'http://10.31.27.207:8776/v2/d5785e4393ba4db5871c34b6a6c3ef7b'

version='2'
uname=
pwd=
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
		#print vlist[1]
		#print vlist[0].__dict__
		#pdb.set_trace()
		result = {}
		result['volumes']=[]
		for i in range(len(vlist)):
			vdict=(vlist[i].__dict__)
			vol = {} #vol=[]
			vol['id'] = vdict['id']#vol.append(vdict['id'].encode('ascii','ignore'))
			vol['name'] = vdict['name']#vol.append(vdict['name'].encode('ascii','ignore'))
			vol['links'] = vdict['links']#vol.append(vdict['size'])
			#print vol
			result['volumes'].append(vol)
		return json.dumps(result),200
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204


######list volumes with whole detail
def get_volumes_detail(con):
	try:  
		vlist=con.volumes.list()
		dvols={}
		dvols['volumes']=[]
		for i in range(len(vlist)):
			vdict=vlist[i].__dict__
			dvols['volumes'].append(vdict)
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
		result={}
		result['voulmes']=vol.__dict__
		return str(result),200
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
          
#####create snapshot for a volume
def create_snapshot(con,uuid):
	try:
		vid=unicode(uuid)
		print type(vid)
		snp=con.volume_snapshots.create(vid,force=True)
		snap=snp.__dict__
		return str(snap),202
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204


#####get summary of snapshots
def get_snapshots(con):
	try:  
		slist=con.volume_snapshots.list()
		result={}
		result['snapshots']=[]
		for i in range(len(slist)):
			sdict=(slist[i].__dict__)
			snp = {} #vol=[]
			snp['status'] = sdict['status']
			snp['description'] = sdict['description'] 
			snp['created_at'] = sdict['created_at']
			snp['metadata'] = sdict['metadata']
			snp['volume_id'] = sdict['volume_id']
			snp['size'] = sdict['size']
			snp['id'] = sdict['id']
			snp['name'] = sdict['name']
			result['snapshots'].append(snp)
		return json.dumps(result)
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
#####POST: curl -X POST http://localhost:5003/v2/EC500-openstack-passthru/volumes -H "Volume-Name:test4" -H "Volume-Size:1"		
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
def func4(tenid,vid):
#####curl -X POST http://localhost:5003/v2/EC500-openstack-passthru/volumes/177e0e61-1c66-4454-b170-aafd99fa2c86/action -H "Volume-Size:11"

	if request.method == 'POST':
		con=connect_cinder()
		size=int(request.headers.get('Volume-Size'))
		return extend_volume(con,vid,size);
	else:
		return "No Such Function", 501



@app.route("/v2/<tenid>/snapshots", methods=['POST', 'GET'])
def func5(tenid):
#####POST: curl -X POST http://localhost:5003/v2/EC500-openstack-passthru/snapshots -H "Volume-id:177e0e61-1c66-4454-b170-aafd99fa2c86"
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/snapshots 

	if request.method == 'POST':
		con=connect_cinder()
		uuid=request.headers.get('Volume-id')
		return create_snapshot(con,uuid)
	elif request.method == 'GET':###to be implemented
		con=connect_cinder()
		return get_snapshots(con)
	else:
		return "No Such Function", 501






if __name__ == "__main__":
        app.run(None,5003,True)
