from os import setuid,setgid,path
from json import load
import socket
import select
def handleIdent(fd):
	data=fd.recv(1024).strip()
	ports=data.split(',',2)
	ports=map(validPort,ports)
	if len(ports)<2 or (not ports[0] or not ports[1]):
		fd.send('0,0 : ERROR : INVALID-PORT')
	else:
		fd.send(data + ' : USERID : '+settings['os']+' : '+settings['user'])
	fd.send('\r\n')
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
		print(str(pair[0])+'and'+str(pair[1]))
		servers[-1].bind((pair[0], pair[1]))
		servers[-1].listen(5)
		servers[-1].setblocking(0)
	setgid(settings['setgid'])
	setuid(settings['setuid'])
	while True:
		inready,outready,excready=select.select(servers,[],[])
		for ready in inready:
			client,addr=ready.accept()
			handleIdent(client)