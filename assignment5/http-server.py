import base64
import hashlib
import socket
import threading


class HttpServer (threading.Thread):
    BUFFER_SIZE = 4096
    CRLF = '\r\n'
    WEBSOCKET_MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def __init__(self, port=8080):
        threading.Thread.__init__(self)
        self.websocket_connections = []
        self.host = ''
        self.port = port
        self.www_dir = '.'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.wait_for_connections()
        finally:
            self.socket.close()

    def wait_for_connections(self):
        while True:
            self.socket.listen()
            connection, address = self.socket.accept()
            data = connection.recv(self.BUFFER_SIZE)
            request = data.decode('UTF-8')
            self.dispatch_request(request, connection)

    def gen_header(self, code, sec_websocket_key=''):
        header_fields = {
            200: ['HTTP/1.1 200 OK'],
            101: ['HTTP/1.1 101 Switching Protocols',
                  'Upgrade: websocket',
                  'Connection: Upgrade',
                  'Sec-WebSocket-Accept: %s' % sec_websocket_key],
            404: ['HTTP/1.1 404 Not Found']
        }[code]
        return '%s%s%s' % (self.CRLF.join(header_fields), self.CRLF, self.CRLF)

    def dispatch_request(self, request, connection):
        header_fields = request.split(self.CRLF)
        method_field = header_fields[0].split(' ')
        {
            '/': lambda: self.handle_index(connection),
            '/index.html': lambda: self.handle_index(connection),
            '/websocket': lambda: self.handle_websocket(connection, request)
        }.get(method_field[1], lambda: self.handle_not_found(connection))()

    def handle_index(self, connection):
        self.serve_file('index.html', connection)

    def handle_websocket(self, connection, request):
        sec_websocket_accept = self.gen_sec_websocket_accept(request)
        response = self.gen_header(101, sec_websocket_accept).encode()
        connection.sendall(response)
        self.websocket_connections.append(connection)

    def handle_not_found(self, connection):
        response = self.gen_header(404).encode()
        connection.sendall(response)
        connection.close()

    @staticmethod
    def calculate_payload_length(payload):
        payload_len = len(payload)
        if payload_len < 126:
            return payload_len.to_bytes(1, 'big')
        elif payload_len < pow(2, 16):
            return (126).to_bytes(1, 'big') + payload_len.to_bytes(2, 'big')
        else:
            return (127).to_bytes(1, 'big') + payload_len.to_bytes(8, 'big')

    def gen_sec_websocket_accept(self, request):
        key = request.split('Sec-WebSocket-Key: ')[1].split(self.CRLF)[0]
        plain = ('%s%s' % (key, self.WEBSOCKET_MAGIC_STRING)).encode()
        hashed = hashlib.sha1(plain).digest()
        return base64.b64encode(hashed).decode()

    def gen_websocket_frame_header(self, payload):
        payload_length = self.calculate_payload_length(payload)
        return b'\x81' + payload_length

    def serve_file(self, file_name, connection):
        file_path = '%s/%s' % (self.www_dir, file_name)
        with open(file_path, 'rb') as file_handler:
            header = self.gen_header(200)
            file = file_handler.read()
            response = header.encode() + file
            connection.sendall(response)

    def broadcast(self, msg):
        payload = msg.encode()
        header = self.gen_websocket_frame_header(payload)
        frame = header + payload
        for connection in self.websocket_connections:
            try:
                connection.sendall(frame)
            except BrokenPipeError:
                connection.close()
                self.websocket_connections.remove(connection)


if __name__ == '__main__':
    http_server = HttpServer()
    http_server.daemon = True
    http_server.start()
    while True:
        http_server.broadcast(input('Message: '))
