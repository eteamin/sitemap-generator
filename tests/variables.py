

host, port = 'localhost', 8686
expected_sitemap = '''<urlset>
    <url>
        <loc>http://{}:{}</loc>
    </url>
    <url>
        <loc>http://{}:{}/full</loc>
    </url>
    <url>
        <loc>http://{}:{}/inner</loc>
    </url>
</urlset>'''.format(*3 * (host, port))
