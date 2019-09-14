import urllib.request
from bs4 import BeautifulSoup

def get_img_srcs(url):
    site = urllib.request.urlopen(url)
    site_bytes = site.read()
    site_str = site_bytes.decode("utf8")

    site_soup = BeautifulSoup(site_str, 'html.parser')

    site_imgs = site_soup.find_all('img')
    img_srcs = []

    for img in site_imgs:
        img_srcs.append(img['src'])

    site.close()

    return img_srcs