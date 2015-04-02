import os
import socket
#from swiftclient import client
from keystoneclient.v2_0 import client
usr = 'singh1'
key = 'JRARJNS'
authurl = 'http://140.247.152.207:35357/v2.0'			
ten = 'EC500-openstack-passthru'


def connect_keystone():			###get authentication token for POST commands.
	
	try:
		con = client.Client(username=usr, password=key,tenant_name=ten,auth_url=authurl)	###need to make jason file for credentials.
		return con
	except ClientException as e:
                return e.msg, e.http_status
	else:

		return "", 204

from swiftclient import ClientException



##################################################################################################### flask:

from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def token():
	
	if request.method == 'POST':
		con = connect_keystone()
		return str(con.auth_ref)
	
	else:
		return "Not yet implemented", 501

if __name__ == "__main__":
        app.run(None,5002,None)
