
from http.server import BaseHTTPRequestHandler

from tests.variables import host, port


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            body = '''<blah></blah>
                <a href="http://{}:{}">github</a>
                <blah></blah>
                <a href="/inner>I am relative</a>
                <blah></blah>'''.format(host, port)
            self.wfile.write(bytes(body, "utf8"))

        elif self.path == '/inner':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            body = '''<blah></blah>
                <a href="http://{}:{}">github</a>
                <a href="http://foreign.url>Foreign url</a>
                <blah></blah>'''.format(host, port)
            self.wfile.write(bytes(body, "utf8"))

        else:
            self.send_response(404)
