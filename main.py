import argparse
from os.path import exists, join
from os import getcwd, mkdir


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enter the url')
    parser.add_argument('-u', '--url', help='Url of the target website', required=True)
    parser.add_argument('-p', '--path', help='Where to store the file', required=False)
    parser.add_argument('-t', '--timeout', help='Request timeout', required=False)

    args = parser.parse_args()
    url = args.url
    path = args.path or join(getcwd(), 'output')
    timeout = int(args.timeout or 3)

    if not url.startswith('http'):
        raise Exception('Url must start with http')

    if not exists(path):
        mkdir(path)

    try:
        import requests
    except ImportError:
        raise Exception('requests module is not installed. `pip install requests`')

    from src.sitemap_generator.crawler import SitemapGenerator

    generator = SitemapGenerator(url=url, timeout=timeout, path=path)
    generator.generate()
