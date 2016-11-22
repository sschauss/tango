import socket
import sys
import gzip
from urllib.parse import urlparse

# Some separators as defined by HTTP standards
CRLF = str(bytes([13, 10]))
TERMINATOR = bytes([13, 10, 13, 10])


def get(url, port=80, buffersize=4096, encoding="UTF-8"):
    """HTTP GETs the given URL and returns the raw data response"""
    data = bytearray()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as httpsock:
        httpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        httpsock.connect((url.hostname, port))

        # Make the request, getting path and query from the location, accepting
        # compress gzip encoding (and identity)
        request = CRLF.join([
            "GET %s?%s HTTP/1.0" % (url.path, url.query),
            "Host: %s" % url.netloc,
            "Accept-Encoding: compress, gzip"
        ])

        # Send the entire request
        httpsock.sendall(request.encode(encoding) + TERMINATOR)

        # Read response into buffer until end
        while True:
            buffer = httpsock.recv(buffersize)
            data += buffer
            if not buffer:
                break

    return data


def decoderesponse(data, encoding="UTF-8"):
    """Parses the data of a HTTP response, returns: header, body"""
    # The terminator separates header and body, find it's position
    pos = data.index(TERMINATOR)

    # Split data at that point, only decode header, as it might be a binary
    # file
    return data[:pos].decode(encoding), data[pos + len(TERMINATOR):]


def program(arg):
    """Reads from the argument an URL and downloads it into a header file and
    the raw content"""
    # Extract input and output parameters from argument
    url = urlparse(arg)
    filename = url.path.split("/")[-1]

    # Perform HTTP get via new socket
    data = get(url)

    # Catch responses that are not covered
    if not data.startswith(b"HTTP/1.1 200 OK"):
        print("HTTP request is not OK, encoded response below:")
        print(data.decode())
        return

    # Parse response and write output
    header, body = decoderesponse(data)

    print(header)
    writeheader(filename, header)
    writebody(filename, header, body)


def writeheader(filename, header):
    """Writes the header file as a text file"""
    with open("%s.header" % filename, "w") as handle:
        handle.write(header)


def writebody(filename, header, body):
    """Writes the body file, if response is gzip compressed, decompresses it"""
    if "Content-Encoding: gzip" in header:
        with open(filename, "wb") as handle:
            handle.write(gzip.decompress(body))
    else:
        with open(filename, "wb") as handle:
            handle.write(body)


# Main application entry points
if __name__ == '__main__':
    program(sys.argv[1])
