#!/usr/bin/python

import json
import socket

IP = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
try:
    name = input('Name: ')
    age = input('Age: ')
    matrikelnummer = input('Matrikelnummer: ')
    data = json.dumps(
            {
                'name': name,
                'age': age,
                'matrikelnummer': matrikelnummer
            }).encode('UTF-8')
    client_socket.sendall(data)
finally:
    client_socket.close()