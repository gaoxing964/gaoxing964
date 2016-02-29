import socket

server = ('192.168.10.202',20072)

socket = socket.socket(socket.AF_INEF,socket.SOCK_STREAM)
socket.bind(server)
socket.listen(5)
conn,address = socket.accept()
while true :
	data = conn.recv(1024)
	if not data : break	
	conn.send(data)
socket.close()