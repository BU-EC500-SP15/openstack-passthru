import os
import socket
import json
import pdb
import copy
from lxml import etree
from oslo_config import cfg
from cinderclient import client

con = cfg.CONF

_KNOW_VERSIONS = {
    "v1.0": {
        "status": "CURRENT",
        "updated": "",
        "id": "v1.1.1",
        "links":[
            {
                "href": "http://140.247.152.207:35357/v1.0",
                "rel": "ywang121"
            },
        ],
        "media-types": [
            {
                "base": "application/json",
                "type": "application/vnd.openstack.volume + json; version = 1"
            },
            {
                "base": "application/xml",
                "type": "application/vnd.openstack.volume + json; version = 1"
            }
        ],
    },
    {
        "status": "CURRENT",
        "update": "",
        "id": "v2.0",
        "links": [
            {
                "href": "http://140.247.152.207:35357/v2.0",
                "rel": "ywang121"
            },
        ],
        "media-types": [
            {
                "base": "application/json",
                "type": "application/vnd.openstack.volume + json; version = 1"
            },
            {
                "base": "application/xml",
                "type": "application/vnd.openstack.volume + json; version = 1"
            }
        ],
    },
}

def get_supported_versions():
    versions = {}
    
    if con.enable_v1_api:
        versions['v1.0'] = _KNOWN_VERSIONS['v1.0']
    if con.enable_v2_api:
        versions['v2.0'] = _KNOWN_VERSIONS['V2.0']

    return versions


def make_version(elem):
    elem.set('id')
    elem.set('status')
    elem.set('updated')
    ...

#########################
# for multiple back-end #
#########################

def Hash(volume):       #should change volume to volume.id
	c_cinder = str(volume).split('-')
	if c_cinder[0] == 'MOC1':
		#print 'in 1'
		return url['MOC1']
	elif c_cinder[0] == 'MOC2':
		#print 'in 2'
		return url['MOC2']
	else:
		sm = 0
		for letters in volume:
			sm += ord(letters)
		index = sm % Backends
		if index == 0: 
			#print 'in 1'
			return url['MOC1']
		elif index == 1:
			#print 'in 2'
			return url['MOC2']

