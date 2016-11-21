import sys
import os
from urllib.parse import urlparse
import re

HTTP_CLIENT = 'http-client.py'

if __name__ == '__main__':
    file_name = sys.argv[1]
    url = urlparse(sys.argv[2])
    data = ''
    with open(file_name) as file:
        data = file.read()
    img_srcs = map(lambda s: re.findall('src="[^"]*"', s)[0][5:-1], re.findall('<img[^>]*/>', data))
    for src in img_srcs:
        if str.startswith(src, 'http') or str.startswith(src, 'https'):
            os.system('python %s %s' % (HTTP_CLIENT, src))
        else:
            os.system('python %s %s://%s%s' % (HTTP_CLIENT, url.scheme, url.hostname, src))
