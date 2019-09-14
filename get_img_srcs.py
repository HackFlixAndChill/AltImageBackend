import urllib.request
from urllib.parse import urlparse
from html.parser import HTMLParser
from html.entities import name2codepoint

def fix_url(src, root_url):
    if(src[0:4] != 'http'):

        if(src[0:2] == '//'):
            return 'https:' + src

        elif(src[0:5] == 'data:'):
            return src
            
        else:
            return root_url + src
    
    return src

class MyHTMLParser(HTMLParser):

    def __init__(self, root_url):
        HTMLParser.__init__(self)
        self.srcs = set()
        self.root_url = root_url

    def handle_starttag(self, tag, attrs):
        if(tag == 'img'):
            for attr in attrs:
                if(attr[0] == 'src'):
                    self.srcs.add(fix_url(attr[1], self.root_url))

def get_img_srcs(url):
    site = urllib.request.urlopen(url)
    site_bytes = site.read()
    site_str = site_bytes.decode('ANSI')

    parsed_url = urlparse(url)
    root_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)

    html_parser = MyHTMLParser(root_url)
    html_parser.feed(site_str)
    srcs = html_parser.srcs

    site.close()

    return srcs

get_img_srcs('https://jccsst-random.blogspot.com/search?updated-max=2019-05-27T19:50:00-04:00&max-results=10')