from queue import Queue, Empty
from threading import Thread
import re
from urllib.parse import urlparse

from requests import get as fetch

from src.sitemap_generator.variables import url_pattern
from src.sitemap_generator.url import URL


class SitemapGenerator(object):

    def __init__(self, url, queue_max_size=500, timeout=3, workers=4):
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
        self.sitemap = ''

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
                url = self.urls.get(timeout=self.timeout)
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
        return fetch(url, timeout=self.timeout).text

    def _build_xml(self):
        self.sitemap += '<urlset>\n'

        for url in self.unique_urls:
            self.sitemap += '    <url>\n'
            self.sitemap += '        <loc>{}</loc>\n'.format(url)
            self.sitemap += '    </url>\n'
        self.sitemap += '</urlset>'

        with open('sitemap.xml', 'w') as sitemap:
            sitemap.write(self.sitemap)
