import os
import socket
from cinderclient import client
from cinderclient.v2 import volume_snapshots
import json
import pdb
import copy

#cinderurl= 'http://10.31.27.207:8776/v2/d5785e4393ba4db5871c34b6a6c3ef7b'

version='2'
uname=''
pwd=''
ten = 'EC500-openstack-passthru'
authurl = 'http://140.247.152.207:35357/v2.0'
authurl_2 = 'http://140.247.152.207:35357/v2.0'       #smae to authurl1 but give a choice #+++

url = {}
url['MOC1'] = 'http://140.247.152.207:8776/v1/d5785e4393ba4db5871c34b6a6c3ef7b'
url['MOC2'] = 'http://140.247.152.207:8776/v1/d5785e4393ba4db5871c34b6a6c3ef7b'
preauth_url= 'http://140.247.152.207:8776/v2/d5785e4393ba4db5871c34b6a6c3ef7b'
preauth_url_2 = 'http://140.247.152.207:8776/v2/d5785e4393ba4db5871c34b6a6c3ef7b'       #give choice #+++

#token='MIIT3QYJKoZIhvcNAQcCoIITzjCCE8oCAQExCTAHBgUrDgMCGjCCEjMGCSqGSIb3DQEHAaCCEiQEghIgeyJhY2Nlc3MiOiB7InRva2VuIjogeyJpc3N1ZWRfYXQiOiAiMjAxNS0wNC0yN1QwNDo0MTowMi4wMDI1NzQiLCAiZXhwaXJlcyI6ICIyMDE1LTA0LTI3VDA1OjQxOjAxWiIsICJpZCI6ICJwbGFjZWhvbGRlciIsICJ0ZW5hbnQiOiB7ImRlc2NyaXB0aW9uIjogIiIsICJlbmFibGVkIjogdHJ1ZSwgImlkIjogImQ1Nzg1ZTQzOTNiYTRkYjU4NzFjMzRiNmE2YzNlZjdiIiwgIm5hbWUiOiAiRUM1MDAtb3BlbnN0YWNrLXBhc3N0aHJ1In19LCAic2VydmljZUNhdGFsb2ciOiBbeyJlbmRwb2ludHMiOiBbeyJhZG1pblVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3Ojg3NzQvdjIvZDU3ODVlNDM5M2JhNGRiNTg3MWMzNGI2YTZjM2VmN2IiLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3Ojg3NzQvdjIvZDU3ODVlNDM5M2JhNGRiNTg3MWMzNGI2YTZjM2VmN2IiLCAiaWQiOiAiNGMwZGI1ZmFlNzkxNDU4NGEwMTc4ZjY5NDE4YmQyYzYiLCAicHVibGljVVJMIjogImh0dHA6Ly8xNDAuMjQ3LjE1Mi4yMDc6ODc3NC92Mi9kNTc4NWU0MzkzYmE0ZGI1ODcxYzM0YjZhNmMzZWY3YiJ9XSwgImVuZHBvaW50c19saW5rcyI6IFtdLCAidHlwZSI6ICJjb21wdXRlIiwgIm5hbWUiOiAibm92YSJ9LCB7ImVuZHBvaW50cyI6IFt7ImFkbWluVVJMIjogImh0dHA6Ly8xMC4zMS4yNy4yMDc6OTY5Ni8iLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3Ojk2OTYvIiwgImlkIjogIjBjNDU2NTcxZDAzZjQzOWM4ZWJhY2YwOWE0OTZlM2JiIiwgInB1YmxpY1VSTCI6ICJodHRwOi8vMTQwLjI0Ny4xNTIuMjA3Ojk2OTYvIn1dLCAiZW5kcG9pbnRzX2xpbmtzIjogW10sICJ0eXBlIjogIm5ldHdvcmsiLCAibmFtZSI6ICJuZXV0cm9uIn0sIHsiZW5kcG9pbnRzIjogW3siYWRtaW5VUkwiOiAiaHR0cDovLzEwLjMxLjI3LjIwNzo4Nzc2L3YyL2Q1Nzg1ZTQzOTNiYTRkYjU4NzFjMzRiNmE2YzNlZjdiIiwgInJlZ2lvbiI6ICJSZWdpb25PbmUiLCAiaW50ZXJuYWxVUkwiOiAiaHR0cDovLzEwLjMxLjI3LjIwNzo4Nzc2L3YyL2Q1Nzg1ZTQzOTNiYTRkYjU4NzFjMzRiNmE2YzNlZjdiIiwgImlkIjogIjBjMGQyNmU1OWZiZDQ4MTVhMzAwZWM1OTI4ODBlYzcyIiwgInB1YmxpY1VSTCI6ICJodHRwOi8vMTQwLjI0Ny4xNTIuMjA3Ojg3NzYvdjIvZDU3ODVlNDM5M2JhNGRiNTg3MWMzNGI2YTZjM2VmN2IifV0sICJlbmRwb2ludHNfbGlua3MiOiBbXSwgInR5cGUiOiAidm9sdW1ldjIiLCAibmFtZSI6ICJjaW5kZXJ2MiJ9LCB7ImVuZHBvaW50cyI6IFt7ImFkbWluVVJMIjogImh0dHA6Ly8xMC4zMS4yNy4yMjMvc3dpZnQvdjEiLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjIzL3N3aWZ0L3YxIiwgImlkIjogIjNhZjM0ZGVmZjNhMjQ5MWJhZjRkZmMyNGRjYjAwMjJlIiwgInB1YmxpY1VSTCI6ICJodHRwOi8vMTQwLjI0Ny4xNTIuMjIzL3N3aWZ0L3YxIn1dLCAiZW5kcG9pbnRzX2xpbmtzIjogW10sICJ0eXBlIjogInMzIiwgIm5hbWUiOiAic3dpZnRfczMifSwgeyJlbmRwb2ludHMiOiBbeyJhZG1pblVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3OjkyOTIiLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3OjkyOTIiLCAiaWQiOiAiNTgzMDhkOGMxOGFlNGViZDgzZGJjZDE2NDE5MzVkZGIiLCAicHVibGljVVJMIjogImh0dHA6Ly8xNDAuMjQ3LjE1Mi4yMDc6OTI5MiJ9XSwgImVuZHBvaW50c19saW5rcyI6IFtdLCAidHlwZSI6ICJpbWFnZSIsICJuYW1lIjogImdsYW5jZSJ9LCB7ImVuZHBvaW50cyI6IFt7ImFkbWluVVJMIjogImh0dHA6Ly8xMC4zMS4yNy4yMDc6ODM4Ni8iLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3OjgzODYvIiwgImlkIjogIjBhMjQxZjBlMThmMDQwOWM4ODc0ZGQwNzg3OTYxZjJmIiwgInB1YmxpY1VSTCI6ICJodHRwOi8vMTQwLjI0Ny4xNTIuMjA3OjgzODYvIn1dLCAiZW5kcG9pbnRzX2xpbmtzIjogW10sICJ0eXBlIjogImRhdGFfcHJvY2Vzc2luZyIsICJuYW1lIjogInNhaGFyYSJ9LCB7ImVuZHBvaW50cyI6IFt7ImFkbWluVVJMIjogImh0dHA6Ly8xMC4zMS4yNy4yMDc6ODAwMC92MS8iLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3OjgwMDAvdjEvIiwgImlkIjogIjI3NTJjMzk1YWRmMzQ0Y2M5MGE3MGFkMzQzZDQ3MjU5IiwgInB1YmxpY1VSTCI6ICJodHRwOi8vMTQwLjI0Ny4xNTIuMjA3OjgwMDAvdjEvIn1dLCAiZW5kcG9pbnRzX2xpbmtzIjogW10sICJ0eXBlIjogImNsb3VkZm9ybWF0aW9uIiwgIm5hbWUiOiAiaGVhdC1jZm4ifSwgeyJlbmRwb2ludHMiOiBbeyJhZG1pblVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3Ojg3NzciLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3Ojg3NzciLCAiaWQiOiAiYWQ1ZmNhNzk2ZDg2NGZhZDkwNjlhZjA5MDY2YjdmM2UiLCAicHVibGljVVJMIjogImh0dHA6Ly8xNDAuMjQ3LjE1Mi4yMDc6ODc3NyJ9XSwgImVuZHBvaW50c19saW5rcyI6IFtdLCAidHlwZSI6ICJtZXRlcmluZyIsICJuYW1lIjogImNlaWxvbWV0ZXIifSwgeyJlbmRwb2ludHMiOiBbeyJhZG1pblVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3Ojg3NzYvdjEvZDU3ODVlNDM5M2JhNGRiNTg3MWMzNGI2YTZjM2VmN2IiLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3Ojg3NzYvdjEvZDU3ODVlNDM5M2JhNGRiNTg3MWMzNGI2YTZjM2VmN2IiLCAiaWQiOiAiNDk3MTI1NWFhNzMwNGNjNzgwMjJmODA0NWViNTMwMGYiLCAicHVibGljVVJMIjogImh0dHA6Ly8xNDAuMjQ3LjE1Mi4yMDc6ODc3Ni92MS9kNTc4NWU0MzkzYmE0ZGI1ODcxYzM0YjZhNmMzZWY3YiJ9XSwgImVuZHBvaW50c19saW5rcyI6IFtdLCAidHlwZSI6ICJ2b2x1bWUiLCAibmFtZSI6ICJjaW5kZXIifSwgeyJlbmRwb2ludHMiOiBbeyJhZG1pblVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3Ojg3NzMvc2VydmljZXMvQWRtaW4iLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3Ojg3NzMvc2VydmljZXMvQ2xvdWQiLCAiaWQiOiAiOTQ5M2U1NmI4NmEwNDhhMTg5M2MwMjhiYjU2ZDEyMDEiLCAicHVibGljVVJMIjogImh0dHA6Ly8xNDAuMjQ3LjE1Mi4yMDc6ODc3My9zZXJ2aWNlcy9DbG91ZCJ9XSwgImVuZHBvaW50c19saW5rcyI6IFtdLCAidHlwZSI6ICJlYzIiLCAibmFtZSI6ICJub3ZhX2VjMiJ9LCB7ImVuZHBvaW50cyI6IFt7ImFkbWluVVJMIjogImh0dHA6Ly8xMC4zMS4yNy4yMDc6ODAwNC92MS9kNTc4NWU0MzkzYmE0ZGI1ODcxYzM0YjZhNmMzZWY3YiIsICJyZWdpb24iOiAiUmVnaW9uT25lIiwgImludGVybmFsVVJMIjogImh0dHA6Ly8xMC4zMS4yNy4yMDc6ODAwNC92MS9kNTc4NWU0MzkzYmE0ZGI1ODcxYzM0YjZhNmMzZWY3YiIsICJpZCI6ICI2ZTk0Y2ZiNDVkOTQ0MGZhOGFhZjE4NjRiOWUyYjA1YiIsICJwdWJsaWNVUkwiOiAiaHR0cDovLzE0MC4yNDcuMTUyLjIwNzo4MDA0L3YxL2Q1Nzg1ZTQzOTNiYTRkYjU4NzFjMzRiNmE2YzNlZjdiIn1dLCAiZW5kcG9pbnRzX2xpbmtzIjogW10sICJ0eXBlIjogIm9yY2hlc3RyYXRpb24iLCAibmFtZSI6ICJoZWF0In0sIHsiZW5kcG9pbnRzIjogW3siYWRtaW5VUkwiOiAiaHR0cDovLzEwLjMxLjI3LjIyMy9zd2lmdC92MSIsICJyZWdpb24iOiAiUmVnaW9uT25lIiwgImludGVybmFsVVJMIjogImh0dHA6Ly8xMC4zMS4yNy4yMjMvc3dpZnQvdjEiLCAiaWQiOiAiNTYzYzE0NTQyZjBjNGJjNzlmNTI5ZjRmY2Y2ZjBjYjEiLCAicHVibGljVVJMIjogImh0dHA6Ly8xNDAuMjQ3LjE1Mi4yMjMvc3dpZnQvdjEifV0sICJlbmRwb2ludHNfbGlua3MiOiBbXSwgInR5cGUiOiAib2JqZWN0LXN0b3JlIiwgIm5hbWUiOiAic3dpZnQifSwgeyJlbmRwb2ludHMiOiBbeyJhZG1pblVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3OjM1MzU3L3YyLjAiLCAicmVnaW9uIjogIlJlZ2lvbk9uZSIsICJpbnRlcm5hbFVSTCI6ICJodHRwOi8vMTAuMzEuMjcuMjA3OjUwMDAvdjIuMCIsICJpZCI6ICIwNjYxOTY3M2M5NmI0NGE5YWRiNGYwODI1N2JiOTBiMCIsICJwdWJsaWNVUkwiOiAiaHR0cDovLzE0MC4yNDcuMTUyLjIwNzo1MDAwL3YyLjAifV0sICJlbmRwb2ludHNfbGlua3MiOiBbXSwgInR5cGUiOiAiaWRlbnRpdHkiLCAibmFtZSI6ICJrZXlzdG9uZSJ9XSwgInVzZXIiOiB7InVzZXJuYW1lIjogImVzdGhlcmx1IiwgInJvbGVzX2xpbmtzIjogW10sICJpZCI6ICIwMjRmNGVhYjI1YmQ0ZjBlODZkNjYzNzExMWFhOTVkMCIsICJyb2xlcyI6IFt7Im5hbWUiOiAiX21lbWJlcl8ifSwgeyJuYW1lIjogIlN3aWZ0T3BlcmF0b3IifV0sICJuYW1lIjogImVzdGhlcmx1In0sICJtZXRhZGF0YSI6IHsiaXNfYWRtaW4iOiAwLCAicm9sZXMiOiBbIjlmZTJmZjllZTQzODRiMTg5NGE5MDg3OGQzZTkyYmFiIiwgImMzMjM5NWIwYWM1YzRmOTI5YjhiNTM3YjBjNzA3ZGU2Il19fX0xggGBMIIBfQIBATBcMFcxCzAJBgNVBAYTAlVTMQ4wDAYDVQQIDAVVbnNldDEOMAwGA1UEBwwFVW5zZXQxDjAMBgNVBAoMBVVuc2V0MRgwFgYDVQQDDA93d3cuZXhhbXBsZS5jb20CAQEwBwYFKw4DAhowDQYJKoZIhvcNAQEBBQAEggEAPvG44uc8rXokkntgHTKZKNUlTyrW6zmb-lVOxCdJDYlOxxyDtaH+9AfgelvHUwfSUNFK0UiTyuWp+s7pfyX6HzZANP4q-j7cJXzj6sH8jgNW294XsSdFV6+Bu75A2kwZYAyNHej+I4lR8uIMK+VpYJZDIL+rgysCGfsaqruwSzyeF62808XuqyTk+zHeNfpa2uIksw2XuZIKtxFwHexF7BwYB9JGC9Ar6mGYrWkmfv1NuCdL6LVwv7bJAZsqseTyjdW7qSaUBEPOK5e7ae-fWSLXz1P0OOK4qmtwHVQWAkr7DdVxtF+Q63SrjB9s8UGDXJcJUU9rfE2S3DBwPmLBfQ=='

    
    

def connect_cinder(): #########works
	con=client.Client(version, uname, pwd , ten, authurl)
	return con
    
def connect_cinder_2():     #+++
    con=client.Client(version, uname, pwd , ten, authurl_2)
    return con
    
####add multi-back-end####
#def connect_cinder_multi(c_url):      #same to "connect_cinder()" but give more choices
#    if url['MOC1'] == c_url:
#        con = client.Client(version, uname, pwd, ten, authurl)
#    elif url['MOC2'] == c_url:
#        con = client.Client(version, uname, pwd, ten, authurl_2)
#    else
#        con = client.Client(version, uname, pwd, ten, authurl_2)
#    return con
####add multi-back-end####

def con_cinder(token,preauthurl):
	con= client.Connection(preauthurl=preauthurl ,preauthtoken=token,auth_version='2', retries=10,)
	return con

####add multi-back-end####
#def con_cinder_multi(token, preauthurl):
#    if preauth_url == preauthurl:
#        con= client.Connection(preauthurl=preauthurl ,preauthtoken=token,auth_version='2', retries=10,)
#    else if preauth_url_2 == preauthurl:
#        con= client.Connection(preauthurl=preauthurl ,preauthtoken=token,auth_version='2', retries=10,)
#    else
#        con= client.Connection(preauthurl=preauthurl ,preauthtoken=token,auth_version='2', retries=10,)
#    return con
####add multi-back-end####

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
		#pdb.set_trace()
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
def create_volume(con,size, snapshot_id, source_volid, name, description, volume_type, availability_zone, metadata, imageRef):
	try:
		p=str(con.volumes.create(size = size, snapshot_id=snapshot_id, source_volid=source_volid, name = name, description = description, volume_type=volume_type, availability_zone=availability_zone, metadata=metadata, imageRef=imageRef))
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
		con.volumes.extend_volume(vol,size)
		result = {}
		result['os-extend']={}
		result['os-extend']['new_size'] = str(size)
		return str(result)
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204
          
#####create snapshot for a volume
def create_snapshot(con,uuid):
	try:
		vid=unicode(uuid)
		#print type(vid)
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

## get summary in detail
def get_snapshots_detail(con):
	try:  
		detail_list=con.volume_snapshots.list()
		result={}
		result['snapshots']=[]
		for i in range(len(detail_list)):
			sdict=(detail_list[i].__dict__)
			result['snapshots'].append(sdict)
		return str(result)
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204

#####delete a snapshot by its uuid
def delete_snapshot(con,snapid):
	try:
		sid=unicode(snapid)
		snap=con.volume_snapshots.get(sid)
		con.volume_snapshots.delete(snap)
		return "",200
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204
		
		
#####get a snapshots whole detail by its uuid
def get_snapshot_id(con,snapid):
	try:
		sid=unicode(snapid)
		snap=con.volume_snapshots.get(sid)
		result={}
		result['snapshot']=snap.__dict__
		return str(result),200
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204
		
#####update snapshot by its uuid
def updates_snapshot(con,snapid,update):
	try:
		pdb.set_trace()
		sid=unicode(snapid)
		snap=con.volume_snapshots.get(sid)
		con.volume_snapshots.update(snap,update)
		result={}
		result['snapshot']=snap.__dict__
		return str(result),200
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204
			

#####get a snapshot's metedata by id
def get_snap_meta(con,snapid):
	try:
		sid=unicode(snapid)
		#print type(vid)
		osnap=con.volume_snapshots.get(sid)
		snap=osnap.__dict__
		snp = {} 
		snp['status'] = snap['status']
		snp['os-extended-snapshot-attributes:progress'] = snap['os-extended-snapshot-attributes:progress']
		snp['description'] = snap['description'] 
		snp['created_at'] = snap['created_at']
		snp['metadata'] = snap['metadata']
		snp['volume_id'] = snap['volume_id']
		snp['os-extended-snapshot-attributes:project_id'] = snap['os-extended-snapshot-attributes:project_id']
		snp['size'] = snap['size']
		snp['id'] = snap['id']
		snp['name'] = snap['name']

		return json.dumps(snp),202
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204


#####
def snap_set_meta(con,snapid,meta): ##########to be modified, now hard coding metadata
	try:
		sid=unicode(snapid)
		#print type(vid)
		print type(meta)
		osnap=con.volume_snapshots.get(sid)
		nmt=con.volume_snapshots.set_metadata(osnap,{"metadata": "vv"})
		print type(nmt)
		ddmt=nmt.__dict__
		dmt=str(ddmt)
		return json.dumps(dmt),200
	except exception as e:
		return e.msg, e.http_status
	else:
		return "", 204

####getting url for backend:   (needs to be tested afer the authentication. should work)
def get_URL(sid):
	for key in url:
		con = connect_cinder(url[key])
		try:
			con.volume_snapshots.get(sid)
			return url[key]
		except :
			pass
	return "Invalid id."

##################################################################################################### flask:

from flask import Flask, request
app = Flask(__name__)


@app.route("/v2/<tenid>/volumes", methods=[ 'GET', 'POST'])
def func1(tenid): 
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/volumes
#####POST: curl -X POST http://localhost:5003/v2/EC500-openstack-passthru/volumes -H"Content-Type:application/json" --data-binary @/home/jj/openstack-passthru/src/Client_json/Vol_JSON
	
        #pdb.set_trace()
	token=request.headers.get('X-Auth-Token')
    if  request.method == 'GET':
		con=con_cinder(token,preauth_url)
		return get_volumes(con)
	elif request.method == "POST":
		con=con_cinder(token,preauth_url)
		if request.headers['Content-Type']=='application/json':
			obj = request.get_json()
			size = obj['volume']['size']
			name = obj['volume']['name']
			availability_zone = obj['volume']['availability_zone']
        		source_volid = obj['volume']['source_volid']
        		description = obj['volume']['description']
        		snapshot_id = obj['volume']['snapshot_id']
        		imageRef = obj['volume']['imageRef']
        		volume_type = obj['volume']['volume_type']
        		metadata = copy.deepcopy(obj['volume']['metadata'])
        		display_name= obj['snapshot']['display_name']
        		display_description= obj['snapshot']['display_description']
        		volume_id= obj['snapshot']['volume_id']
        		force= obj['snapshot']['force']
        		key=obj['snapshot']['key']
                
            ###add multi-back-end choice here###
            if size >= 50:
                con=con_cinder(token,preauth_url_2)
                cre = create_volume(con,size, snapshot_id, source_volid, name, description, volume_type, availability_zone, metadata, imageRef)
                label_1 = "url-" + cre
                return label_1
            elif size < 50:
                cre = create_volume(con,size, snapshot_id, source_volid, name, description, volume_type, availability_zone, metadata, imageRef)
                label_2 = "url_2-" + cre
                return label_2
            else:
                return "Not supported."
            else:
                return "No Such Function", 501
            
            
			#name=request.headers.get('Volume-Name').encode('ascii','ignore')
			#size=int(request.headers.get('Volume-Size'))
			#print type(name)
			#print type(size)
#			return 	create_volume(con,size, snapshot_id, source_volid, name, description, volume_type, availability_zone, metadata, imageRef)
#		else:
#			return "Not supported."
#        else:
#                return "No Such Function", 501



@app.route("/v2/<tenid>/volumes/detail", methods=[ 'GET'])
def func2(tenid): 
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/volumes/detail
	token=request.headers.get('X-Auth-Token')
	if request.method == 'GET':
		con=con_cinder(token,preauth_url)
		return get_volumes_detail(con)
	else:
		return "No Such Function", 501



@app.route("/v2/<tenid>/volumes/<vid>", methods=[ 'GET', 'PUT', 'DELETE'])
def func3(tenid,vid): 
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/volumes/uuid
#####DELETE: curl -X DELETE http://localhost:5003/v2/EC500-openstack-passthru/volumes/uuid
	token=request.headers.get('X-Auth-Token')
	if request.method == 'GET':
		con=con_cinder(token,preauth_url)
		return get_a_volume(con,vid)
	elif request.method == 'PUT':###to be implemented
		con=con_cinder(token,preauth_url)
		return 'not yet'
	elif request.method == 'DELETE':
		con=con_cinder(token,preauth_url)
		return delete_volume(con,vid)
	else:
		return "No Such Function", 501

	

@app.route("/v2/<tenid>/volumes/<vid>/action", methods=[ 'POST'])
def func4(tenid,vid):
#####curl -X POST http://localhost:5003/v2/EC500-openstack-passthru/volumes/17a156af-4aaf-4168-a026-853310435368/action -H"Content-Type:application/json" --data-binary @/home/jj/openstack-passthru/src/Client_json/Vol_extend_JSON
	token=request.headers.get('X-Auth-Token')
	if request.method == 'POST':
		con=con_cinder(token,preauth_url)
		if request.headers['Content-Type']=='application/json':
			obj = request.get_json()
			size = int(obj['os-extend']['new_size'])
			#size=int(request.headers.get('Volume-Size'))
			pdb.set_trace()
			return extend_volume(con,vid,size);
	else:
		return "No Such Function", 501



@app.route("/v2/<tenid>/snapshots", methods=['POST', 'GET'])
def func5(tenid):
#####POST: curl -X POST http://localhost:5003/v2/EC500-openstack-passthru/snapshots -H "Volume-id:177e0e61-1c66-4454-b170-aafd99fa2c86"
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/snapshots 
	token=request.headers.get('X-Auth-Token')
	if request.method == 'POST':
		con=con_cinder(token,preauth_url)
		uuid=request.headers.get('Volume-id')
		return create_snapshot(con,uuid)
	elif request.method == 'GET':
		con=con_cinder(token,preauth_url)
		return get_snapshots(con)
	else:
		return "No Such Function", 501
		
@app.route("/v2/<tenid>/snapshots/detail", methods=[ 'GET'])
def detail(tenid):
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/snapshots/detail
	token=request.headers.get('X-Auth-Token')
	if request.method == 'GET':
		con=con_cinder(token,preauth_url)
		return get_snapshots_detail(con)
	else:
		return "No Such Function", 501


@app.route("/v2/<tenid>/snapshots/<sid>", methods=[ 'GET', 'PUT', 'DELETE'])
def func_uid(tenid,sid): 

#####DELETE: curl -X DELETE http://localhost:5003/v2/EC500-openstack-passthru/snapshots/uuid
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/snapshots/4ebe4c27-97d3-4153-822f-11438f67dcdb
#####PUT: curl -X PUT http://localhost:5003/v2/EC500-openstack-passthru/snapshots/4ebe4c27-97d3-4153-822f-11438f67dcdb -H "name:testj"
	token=request.headers.get('X-Auth-Token')
	if request.method == 'DELETE':
		con=con_cinder(token,preauth_url)
		return delete_snapshot(con,sid)
	elif request.method == 'GET':
		#url = get_URL(sid)
		con=con_cinder(token,preauth_url)
		return get_snapshot_id(con,sid)
	elif request.method == 'PUT':###to be implemented
		con=con_cinder(token,preauth_url)
		head = request.headers
		headers = {}
		for key in head:
			headers[key[0]] = key[1]
		
		return updates_snapshot(con,sid,headers)
		
	else:
		return "No Such Function", 501




@app.route("/v2/<tenid>/snapshots/<snapid>/metadata", methods=['GET','PUT'])
def func6(tenid,snapid):
#####GET: curl -X GET http://localhost:5003/v2/EC500-openstack-passthru/snapshots/9dfd50ea-936f-495b-b14d-b9f3e54599a2/metadata
#####PUT: 
	token=request.headers.get('X-Auth-Token')
	if request.method == 'GET':
		con=con_cinder(token,preauth_url)
		return get_snap_meta(con,snapid)
	elif request.method == 'PUT':###to be implemented
		con=con_cinder(token,preauth_url)
		meta=request.headers.get('Metadata')#format:{"metadata": "v2"}
		return snap_set_meta(con,snapid,meta)
	else:
		return "No Such Function", 501







if __name__ == "__main__":
        app.run(None,5003,True)
Status API Training Shop Blog About
© 2015 GitHub, Inc. Terms Privacy Security Contact
