from os import setuid,setgid,path
from json import load
import dualstack
def handleIdent(fd):
	data=fd.recv(1024).strip()
	ports=data.split(',',2)
	ports=map(validPort,ports)
	if not ports[0] or not ports[1]:
		fd.send('0 , 0 : ERROR : INVALID-PORT')
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
	server = dualstack.MultipleSocketsListener(settings['listeners'])
	setgid(settings['setgid'])
	setuid(settings['setuid'])
	while True:
		conn,addr=server.accept()
		handleIdent(conn)
