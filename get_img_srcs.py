import urllib.request
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
from html.entities import name2codepoint

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

class MyHTMLParser(HTMLParser):
    def __init__(self, root_url):
        HTMLParser.__init__(self)
        self.srcs = set()
        self.root_url = root_url

    def handle_starttag(self, tag, attrs):
        src = ''
        alt = ''
        
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    src = attr[1]
                elif attr[0] == 'alt':
                    alt = attr[1]
                    
            if alt == '':
                self.srcs.add(src)

def fix_url(src, root_url):
    abspath = urljoin(root_url, src)

    if src[0:5] == 'data:':
        return src
    else:    
        return abspath

def get_img_srcs(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    site = urllib.request.urlopen(req)
    site_bytes = site.read()
    site_str = site_bytes.decode('UTF-8')

    parsed_url = urlparse(url)
    root_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)

    html_parser = MyHTMLParser(root_url)
    html_parser.feed(site_str)
    srcs = html_parser.srcs

    # Original URL first, fixed one second
    srcs_with_fixed = {}
    for src in srcs:
        fixed_src = fix_url(src, url)
        srcs_with_fixed.update({fixed_src: fixed_src})

    site.close()

    return srcs_with_fixed
