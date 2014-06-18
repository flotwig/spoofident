from os import setuid,setgid,path
from json import load
from time import time
from select import select
import socket
def handleIdent(fd):
	fd.settimeout(1)
	try:
		data=fd.recv(1024).strip()
	except:
		fd.send('0,0:ERROR:UNKNOWN-ERROR\r\n') # TODO: catch exceptions which are actual errors, as opposed to no-data reports
		return
	ports=data.split(',',2)
	ports=map(validPort,ports)
	if len(ports)<2 or not all(ports):
		fd.send('0,0:ERROR:INVALID-PORT\r\n')
	else:
		fd.send(','.join(map(str,ports))+':USERID:'+settings['os']+':'+settings['user']+'\r\n')
	fd.close()
def validPort(port):
	try:
		port=int(port)
	except ValueError:
		return False
	if port>0 and port<65536:
		return port
	return False
if __name__=='__main__':
	pwd=path.dirname(path.realpath(__file__))
	config=open(pwd+'/spoofident.json','r')
	settings=load(config)
	config.close()
	servers=[]
	for host,port in settings['listeners']:
		if ':' in host: # TODO: write actual ip6 detection, properly?
			servers.append(socket.socket(socket.AF_INET6,socket.SOCK_STREAM))
		else:
			servers.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
		servers[-1].bind((host,port))
		servers[-1].listen(5)
		servers[-1].setblocking(0)
	setgid(settings['setgid'])
	setuid(settings['setuid'])
	while True:
		inready,_,_=select(servers,[],[])
		for ready in inready:
			if ready in servers:
				client,addr=ready.accept()
				inready.append(client)
			else:
				try:
					handleIdent(ready)
				except:
					pass
