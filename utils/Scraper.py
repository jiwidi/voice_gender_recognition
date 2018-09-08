from requests import get
from urllib.parse import urljoin
from os import path, getcwd
from bs4 import BeautifulSoup as soup
from sys import argv
import os.path

url='http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/'

def get_page(base_url):
    req= get(base_url)
    if req.status_code==200:
        return req.text
    raise Exception('Error {0}'.format(req.status_code))

def get_all_links(html):
    bs= soup(html)
    links= bs.findAll('a')
    return links
def get_pdf(base_url, base_dir):
    print('Retrieving urls')
    html= get_page(base_url)
    links= get_all_links(html)
    print('Done retrieving urls')
    if len(links)==0:
        raise Exception('No links found on the webpage')
    n_pdfs= 0
    for link in links:
        if link['href'][-4:]=='.tgz':
            n_pdfs+= 1
            print('Downloading {0}'.format(urljoin(base_url, link['href'])))
            if not (os.path.isfile(path.join(base_dir, link.text))):
                content= get(urljoin(base_url, link['href']))
                if content.status_code==200 and content.headers['content-type']=='application/x-gtar-compressed':
                    with open(path.join(base_dir, link.text), 'wb') as tgz:
                        tgz.write(content.content)
                print('Done')
            else:
                print("Already downloaded")
    if n_pdfs==0:
        raise Exception('No tgz found on the page')
    print ("{0} tgzs files downloaded and saved in {1}".format(n_pdfs, base_dir))


if __name__ == '__main__':
    arg= "rawData/"
    url= 'http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/'
    base_dir= [getcwd(), arg][path.isdir(arg)]

    try:
        get_pdf(url,base_dir)
    except Exception as e:
        print (e)
        exit(-1)
