import os
import shutil
import unittest
from http.server import HTTPServer
from threading import Thread

from tests.sandbox_server import RequestHandler

from sitemap_generator.crawler import SitemapGenerator
from tests.variables import host, port


class TestCase(unittest.TestCase):

    def setUp(self):
        self.background_server = Thread(target=self.server, daemon=True)
        self.background_server.start()
        self.url = 'http://{}:{}'.format(host, port)
        self.output_dir = os.path.join(os.getcwd(), 'tmp')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def test_crawler(self):
        generator = SitemapGenerator(self.url, path=self.output_dir, timeout=None)
        generator.generate()

        with open(os.path.join(self.output_dir, '{}:{}.xml').format(host, port)) as sitemap:
            # FIXME: assertion
            assert sitemap.read() is not None

    def tearDown(self):
        shutil.rmtree(self.output_dir)
        self.sandbox_server.server_close()

    def server(self):
        self.sandbox_server = HTTPServer((host, port), RequestHandler)
        self.sandbox_server.serve_forever()


if __name__ == '__main__':
    unittest.main()
