

class URL(object):
    def __init__(self, url):
        self.url = url

    @property
    def is_relative(self):
        return not self.url.startswith('http')

    @property
    def has_primitive_slash(self):
        return self.url.startswith('/')

    def ensure_primitive_slash(self):
        if not self.has_primitive_slash:
            return '/%s' % self.url
        return self.url

    def get_full_url(self, base_url, domain, scheme='http'):
        if self.url.endswith('/'):
            self.url = self.url[:-1]
        if '#' in self.url:
            return base_url
        elif self.is_relative:
            return '%s://%s%s' % (scheme, domain, self.ensure_primitive_slash())
        elif domain in self.url:
            return self.url
        else:
            return base_url
