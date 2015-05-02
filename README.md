# openstack-passthru
Per-tenant pass-through Openstack services.

By-Jasjot Singh, Dongtai Du, Yigang Wang, Yisi Lu, Shashank Chitti

Environment setup:

1) Insatll a VM (we used ubuntu 14.04 LST) via virtual box, vmware, etc

2) Make sure python 2.7 is insatlled 

3) Insatll python virtual environment, follow the guide lines on the following page:
  
                http://flask.pocoo.org/docs/0.10/installation/#installation
  
  use commands: 
                $ sudo apt-get install python-virtualenv
                $ mkdir myproject
                $ cd myproject
                $ virtualenv venv
                $ . venv/bin/activate
                $ pip install Flask
                $ pip install keystone
                $ pip install python-keystoneclient
                $ pip install python-swiftclient
                $ pip install python-cinderclient
                
4)Make a ssh pubic key and have it registered with MOC.

5)Follow the guide lines on the following page to set up proxy settings.
  
  https://github.com/CCI-MOC/moc-public/wiki/Access-the-OpenStack-dashboard
  
  Port number can be changed as per the user.
  
  Use the following command for SSH Port Forwarding to get access to the SSH-Gateway:(have this running in a seprate terminal in order to access MOC)
    
    $ ssh -D $SOCKS_PORT_NUMBER $BU_USERNAME@140.247.152.200 -N  
    use the same port number as in the proxy settings and the user name after regestring with MOC.
    
6) Insatll proxychanins:
    Use the following commands:
    
    $ sudo apt-get insatll proxychains
    $ mkdir ~/.proxychains
    $ cp /etc/proxychains.confg ~/.proxychains
    $ gedit ~/.proxychains/proxychains.conf
    
    Under the heading [ProxyList]
    Change socks4 127.0.0.1 9050 to socks5 127.0.0.1 $SOCKS_PORT_NUMBER (thats the port number you specified in the proxy settings.)
    
7)Download the code from github: https://github.com/BU-EC500-SP15/openstack-passthru.git

8)In order to run the files use the following commands in the virtual enviornment($ . venv/bin/activate):
  
    $ proxychains python swift-server.py (in a different terminal/tab)
    $ proxychains python keystone-server.py(in a different terminal/tab)
    $ proxychains python cinder-server.py(in a different terminal/tab)
  
9)To test use the curl HTTP requests or the bash variables in the commands folder.:
  
  To test HTTP:
  
  Simple use commds in different terminal.
  
  To test bash variables:
 
  Use commands in a different terminal
  Followed by swift commandline commands - swift list,swift stat, etc.
  
HAPPY RUNNING!!!!
  
