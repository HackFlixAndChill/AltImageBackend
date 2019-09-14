import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from PIL import Image
import requests
from io import BytesIO

def get_imgs(url):
    imgs = {}

    img_srcs = get_img_srcs(url)

    data = []
    for src in img_srcs:
        data = get_img_data(url, src)
        imgs.update({src: data})

    return imgs

def get_img_srcs(url):
    site = urllib.request.urlopen(url)
    site_bytes = site.read()
    site_str = site_bytes.decode('ANSI')

    site_soup = BeautifulSoup(site_str, 'html.parser')

    site_imgs = site_soup.find_all('img')
    img_srcs = []

    for img in site_imgs:
        src = (img['src'])
        if src not in img_srcs:
            img_srcs.append(src)

    parsed_url = urlparse(url)
    root_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)

    for i, src in enumerate(img_srcs):

        if(src[0:4] != 'http'):

            if(src[0:2] == '//'):
                img_srcs[i] = 'https:' + src

            elif(src[0:5] == 'data:'):
                pass
            
            else:
                img_srcs[i] = root_url + src

    # print(root_url)

    site.close()

    # print(site_imgs)
    # print(img_srcs)

    return img_srcs

def get_img_data(url, src):
    img_bytes = []

    parsed_url = urlparse(url)
    root_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)

    # if(src.find('http') != 0):

    #     if(src[0:2] == '//'):
    #         src = 'https:' + src

    #     elif(src[0:5] == 'data:'):
    #         pass

    #     else:
    #         src = root_url + src

    try:
        response = requests.get(src)
        img_bytes = Image.open(BytesIO(response.content))

    except:
        print('ERROR: Could not reach URL ' + src)

    return img_bytes

get_imgs('https://jccsst-random.blogspot.com/search?updated-max=2019-05-27T19:50:00-04:00&max-results=10')