from queue import Queue, Empty
from threading import Thread
import re
import os
from urllib.parse import urlparse

from requests import get as fetch

from src.sitemap_generator.variables import url_pattern
from src.sitemap_generator.url import URL

TIMEOUT = 3


class SitemapGenerator(object):

    def __init__(self, url, path, timeout, queue_max_size=500, workers=4):
        self.base_url = url
        url_parts = urlparse(url)
        self.domain = url_parts.netloc
        self.scheme = url_parts.scheme
        self.timeout = timeout
        self.workers = workers
        self.urls = Queue(maxsize=queue_max_size)
        self.unique_urls = []
        self.urls.put(self.base_url)
        self.worker_threads = {}
        self.path = path

    def generate(self):
        for i in range(self.workers):
            new_thread = Thread(target=self._url_gatherer_worker, daemon=True)
            self.worker_threads[i] = new_thread
            new_thread.start()

        for i, thread in self.worker_threads.items():
            thread.join()

        self._build_xml()

    def _url_gatherer_worker(self):
        while True:
            try:
                url = self.urls.get(timeout=self.timeout or TIMEOUT)
            except Empty:
                break
            self._gather(url)

    def _gather(self, page):
        data = self._fetch(page)

        for i in re.finditer(url_pattern, data, re.DOTALL):
            url = URL(i.groupdict().get('url')).get_full_url(self.base_url, self.domain, self.scheme)
            if url not in self.unique_urls:
                print(url)
                self.unique_urls.append(url)
                self.urls.put(url)

    def _fetch(self, url):
        return fetch(url, timeout=self.timeout or TIMEOUT).text

    def _build_xml(self):
        data = '<urlset>\n'

        for url in self.unique_urls:
            data += '    <url>\n'
            data += '        <loc>{}</loc>\n'.format(url)
            data += '    </url>\n'
        data += '</urlset>'

        self._write_xml(data)

    def _write_xml(self, data):
        with open('{}/{}.xml'.format(self.path, self.domain), 'w+') as sitemap:
            sitemap.write(data)
