import os
import socket
import copy
#from swiftclient import client
from keystoneclient.v2_0 import client

authurl = 'http://140.247.152.207:35357/v2.0'			


def connect_keystone(usr,key,ten):			###get authentication token for POST commands.
	
	try:
		con = client.Client(username=usr, password=key,tenant_name=ten,auth_url=authurl)	###need to make jason file for credentials.
		return con
	except ClientException as e:
                return e.msg, e.http_status
	else:

		return "", 204

#from keystoneclient.v2_0 import ClientException

def redirect(con):			###redirect the keystone endpoints to our proxy servers.
	key =dict(con.auth_ref)
	
	token = {}
	token['token'] = key['token']
	token['version'] = key['version']
	token['serviceCatalog'] = []
	for val in key['serviceCatalog']:
		if (val['name']=='keystone')or(val['name']=='swift'):
			token['serviceCatalog'] .append(val)
	for val in token['serviceCatalog']:
		if(val['name']=='keystone'):
			val['endpoints'][0]['publicURL'] = 'http://localhost:5002'
		elif(val['name']=='swift'):
			val['endpoints'][0]['publicURL'] = 'http://localhost:5000'
	token['user'] = key['user']
	token['metadata'] = key['metadata']	
	#print token['serviceCatalog']
	print key
	return token	
		
	
			


##################################################################################################### flask:

from flask import Flask, request, json
app = Flask(__name__)

@app.route("/v2.0/tokens", methods=['GET', 'POST'])
def token():
	
	if request.method == 'POST':
		if request.headers['Content-Type']=='application/json':
			obj = request.get_json()
			usr = obj['auth']['passwordCredentials']['username']
			key = obj['auth']['passwordCredentials']['password']
			ten = obj['auth']['tenantName']
			con = connect_keystone(usr,key,ten)
			token = redirect(con)
			return str(token)
				 
		else:
			return 'Not Supported Media'
	
	else:
		return "Not yet implemented", 501

if __name__ == "__main__":
        app.run(None,5002,True)
