
# coding: utf-8

# In[ ]:

#!/usr/bin/python
import socket

IP = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(1)
connection, address = server_socket.accept()
data = ''
def parseUrl (url):

    protocol_rest=url.split('://')

    dict_url={}
    dict_url['protocol']=protocol_rest[0]
    host_rest=protocol_rest[1].split('/',1)

    port='Undefined'
    domains=host_rest[0]
    if ':' in domains:
        port_split=domains.split(':')
        domains=port_split[0]
        port=port_split[1]
    dict_url['port']=port
    domain_split=domains.split('.')
    subdomain='Undefined'
    domain=''

    if (len(domain_split)!=2):
        domain_parts=domains.split('.',1)
        subdomain=domain_parts[0]
        domain=domain_parts[1]
    else:
        domain=domains
    dict_url['subdomain']=subdomain
    dict_url['domain']=domain

    path_rest=host_rest[1]
    fragment='Undefined'
    if '#' in path_rest:
        rest_fragment=path_rest.split('#')
        path_rest=rest_fragment[0]
        fragment=rest_fragment[1]
    dict_url['fragment']=fragment

    path=''
    parameters='Undefined'
    if '?' in path_rest:
        path_parameters=path_rest.split('?')
        path=path_parameters[0]
        parameters=path_parameters[1]
    else:
        path=path_rest
    dict_url['path']=path
    dict_url['parameters']=parameters
    return dict_url

try:
    while True:
        buffer = connection.recv(BUFFER_SIZE)
        data += buffer.decode('UTF-8')
        if not buffer:
            dict = parseUrl(data)
            print('Protocol: %s' % dict['protocol'])
            print('Domain: %s' % dict['domain'])
            print('Sub-Domain: %s' % dict['subdomain'])
            print('Port number: %s' % dict['port'])
            print('Path: %s' % dict['path'])
            print('Parameters: %s' % dict['parameters'])
            print('Fragment: %s' % dict['fragment'])
            break
finally:
    server_socket.close()
    
