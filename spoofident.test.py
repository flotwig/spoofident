import socket
from json import load
from sys import argv
targs=argv
targs.pop(0)
message=' '.join(targs)
config=open('./spoofident.json','r')
settings=load(config)
config.close()
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1',113))
print('Sending '+message)
sock.send(message.encode('UTF-8'))
print(sock.recv(1024).decode('UTF-8'))
sock.close()
