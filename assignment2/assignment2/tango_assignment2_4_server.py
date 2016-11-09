#!/usr/bin/python
import socket
import json

IP = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(1)
connection, address = server_socket.accept()
data = ''
try:
    while True:
        buffer = connection.recv(BUFFER_SIZE)
        data += buffer.decode('UTF-8')
        if not buffer:
            dict = json.loads(data)
            print('Name: %s;' % dict['name'])
            print('Age: %s;' % dict['age'])
            print('Matrikelnummer: %s' % dict['matrikelnummer'])
            break
finally:
    server_socket.close()

