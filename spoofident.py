from os import setuid
from json import load
import dualstack
def handleIdent(fd):
	data=fd.recv(1024).strip()
	ports=data.split(',',2)
	ports=map(validPort,ports)
	if not ports[1] or not ports[0]:
		fd.sendall('0 , 0 : ERROR : INVALID-PORT')
		return
	fd.sendall(data + ' : USERID : '+settings['os']+' : '+settings['user'])
def validPort(port):
	port=int(port)
	if port>0 and port<65536:
		return port
	else:
		return False
if __name__ == "__main__":
	config=open('spoofident.json','r')
	settings=load(config)
	config.close()
	server = dualstack.MultipleSocketsListener(settings['listeners'])
	setuid(settings['setuid'])
	while True:
		conn,addr=server.accept()
		handleIdent(conn)
