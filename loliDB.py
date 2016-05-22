import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json

def get():
    content = urllib.request.urlopen("https://www.google.com.tw/search?q=define:OO")
    #content=content.decode('utf8')
    content=content.read()
    content=json.load(content)
    print(content)

    #req =  urllib.request.urlopen('https://www.google.com.tw/search?q=define%3AOO&oq=define%3AOO&gs_l=serp.12...0.0.0.735548.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.C5fRocEpVBU')
    #encoding = req.headers.get_content_charset()
    #obj = json.loads(req.read().decode(encoding))



if __name__=="__main__":
    get()