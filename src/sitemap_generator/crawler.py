from queue import Queue, Empty
from threading import Thread
import re
from urllib.parse import urlparse

from requests import get as fetch

from .variables import url_pattern
from .url import URL


class SitemapGenerator(object):

    def __init__(self, url, queue_max_size=500, timeout=3, workers=4):
        self.base_url = url
        url_parts = urlparse(url)
        self.domain = url_parts.netloc
        self.scheme = url_parts.scheme
        self.timeout = timeout
        self.workers = workers
        self.urls = Queue(maxsize=queue_max_size)
        self.urls_hash = []
        self.urls.put(self.base_url)
        self.worker_threads = {}

    def generate(self):
        for i in range(self.workers):
            new_thread = Thread(target=self._url_gatherer_worker, daemon=True)
            self.worker_threads[i] = new_thread
            new_thread.start()

        for i, thread in self.worker_threads.items():
            thread.join()

    def _url_gatherer_worker(self):
        while True:
            try:
                url = self.urls.get(timeout=self.timeout)
            except Empty:
                break
            self._gather(url)

    def _gather(self, page):
        data = self._fetch(page)

        for i in re.finditer(url_pattern, data, re.DOTALL):
            url = URL(i.groupdict().get('url')).get_full_url(self.domain, self.scheme)
            url_hash = hash(url)
            if url_hash not in self.urls_hash:
                self.urls_hash.append(url_hash)
                self.urls.put(url)

    @staticmethod
    def _fetch(url):
        return fetch(url).text


