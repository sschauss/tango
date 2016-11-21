import socket
import sys
from urllib.parse import urlparse

CRLF = "\r\n\r\n"


def httpGet(url):
    data = bytearray()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as http_socket:
        http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        http_socket.connect((url.hostname, 80))
        request_header = ''
        request_header += 'GET %s?%s HTTP/1.0%s' % (url.path, url.query, CRLF)
        request_header += 'Host: %s %s' % (url.netloc, CRLF)
        request_header += 'Accept-Encoding: compress, gzip%s' % CRLF
        http_socket.sendall(request_header.encode('UTF-8'))
        while True:
            buffer = http_socket.recv(4096)
            data += buffer
            if not buffer:
                break
    return data


def parseHttpResponse(data):
    data_split = ''.join(map(chr, data)).split(CRLF)
    header = CRLF.join(data_split[:-1])
    body = data[(len(header)) + len(CRLF):]
    return header, body


if __name__ == '__main__':
    url = urlparse(sys.argv[1])
    file_name = url.path.split('/')[-1]
    data = httpGet(url)
    header, body = parseHttpResponse(data)

    with open("%s.header" % file_name, 'w') as response_header_file:
        response_header_file.write(header)

    with open(file_name, 'wb') as response_body_file:
        response_body_file.write(body)
