import curses
import json
import re
import os
import time
from threading import Thread
from urllib.parse import urlparse, urljoin, urldefrag
from urllib.request import urlopen


class Crawler:
    POOL_SIZE = 10

    def __init__(self, start_url):
        self.scr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        self.scr.keypad(1)
        self.start_url = urlparse(start_url)
        self.stack = set()
        self.url_to_urls = dict()
        self.error_urls = set()
        self.worker_id_to_working = dict()
        self.compiled_regex = re.compile('<a[^>]+href="([^">]+)"')

    @staticmethod
    def get(url):
        with urlopen(url) as connection:
            return connection.read()

    def extract_urls(self, payload):
        return self.compiled_regex.findall(payload)

    def crawl(self, worker_id):
        while True:
            stack_length = len(self.stack)
            if len(self.stack) == 0 and True not in self.worker_id_to_working.values():
                break
            elif stack_length > 0:
                self.worker_id_to_working[worker_id] = True
                url = self.stack.pop()
                try:
                    document = self.get(url)
                    relative_urls = self.extract_urls(document.decode())
                    absolute_urls = list(map(lambda href: urljoin(url, href), relative_urls))
                    for u in absolute_urls:
                        defraged_u = urldefrag(u).url
                        if defraged_u not in self.url_to_urls and urlparse(u).netloc == self.start_url.netloc:
                            self.stack.add(defraged_u)
                    self.url_to_urls.update({url: absolute_urls})
                    self.write_document(url, document)
                except Exception as e:
                    self.url_to_urls.update({url: str(e)})
                finally:
                    self.worker_id_to_working[worker_id] = False

    @staticmethod
    def write_document(url, document):
        path = './output%s' % urlparse(url).path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as handle:
            handle.write(document)

    def write_statistics(self):
        with open('./statistics.json', 'w') as handle:
            json.dump(self.url_to_urls, handle)

    def log(self):
        start = time.time()
        while True:
            if len(self.stack) == 0 and True not in self.worker_id_to_working.values():
                break
            c_urls_len = len(self.url_to_urls)
            c_stack_len = len(self.stack)
            end = time.time()
            start_end_diff = end - start
            stack_delta_per_second = c_stack_len / start_end_diff
            urls_per_second = c_urls_len / start_end_diff
            self.scr.addstr(0, 0, 'stack size: %i' % c_stack_len)
            self.scr.addstr(1, 0, 'mean stack delta second: %i' % int(stack_delta_per_second))
            self.scr.addstr(2, 0, 'unique urls: %i' % c_urls_len)
            self.scr.addstr(3, 0, 'mean urls per second: %i' % int(urls_per_second))
            self.scr.refresh()
            time.sleep(1 / 10)

    def start(self):
        try:
            self.stack.add(self.start_url.geturl())
            workers = []
            for worker_id in range(0, self.POOL_SIZE):
                thread = Thread(target=self.crawl, args=[worker_id])
                self.worker_id_to_working.update({worker_id: False})
                workers.append(thread)
                thread.start()
            logger = Thread(target=self.log)
            logger.start()
            for thread in workers:
                thread.join()
            logger.join()
            self.write_statistics()
        finally:
            curses.nocbreak()
            self.scr.keypad(0)
            curses.echo()
            curses.endwin()


if __name__ == '__main__':
    crawler = Crawler('http://141.26.208.82/articles/g/e/r/Germany.html')
    # crawler = Crawler(b'http://localhost:8000/index.html')
    crawler.start()
