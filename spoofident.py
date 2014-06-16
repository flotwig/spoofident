from os import setuid,setgid,path
from json import load
from time import time
from select import select
import socket
def handleIdent(fd):
	begin=time()
	fd.setblocking(0)
	data=''
	while time()-begin<1:
		try:
			data=fd.recv(1024).strip()
			if data: break
		except:
			pass # TODO: catch exceptions which are actual errors, as opposed to no-data reports
	ports=data.split(',',2)
	ports=map(validPort,ports)
	if not data:
		fd.send('0,0:ERROR:UNKNOWN-ERROR\r\n')
	elif len(ports)<2 or (not ports[0] or not ports[1]):
		fd.send('0,0:ERROR:INVALID-PORT\r\n')
	else:
		fd.send(str(ports[0])+','+str(ports[1])+':USERID:'+settings['os']+':'+settings['user']+'\r\n')
	fd.close()
def validPort(port):
	try:
		port=int(port)
	except ValueError:
		return False
	if port>0 and port<65536:
		return port
	else:
		return False
if __name__ == '__main__':
	pwd=path.dirname(path.realpath(__file__))
	config=open(pwd+'/spoofident.json','r')
	settings=load(config)
	config.close()
	servers=[]
	for pair in settings['listeners']:
		if ':' in pair[0]: # TODO: write actual ip6 detection, properly?
			servers.append(socket.socket(socket.AF_INET6,socket.SOCK_STREAM))
		else:
			servers.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
		servers[-1].bind((pair[0], pair[1]))
		servers[-1].listen(5)
		servers[-1].setblocking(0)
	setgid(settings['setgid'])
	setuid(settings['setuid'])
	while True:
		inready,outready,excready=select(servers,[],[])
		for ready in inready:
			if ready in servers:
				client,addr=ready.accept()
				inready.append(client)
			else:
				try:
					handleIdent(ready)
				except:
					pass