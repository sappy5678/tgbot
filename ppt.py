import requests
from bs4 import BeautifulSoup
import re
import time

over18_url='https://www.ptt.cc/bbs/Beauty/index.html'

r=requests.Session()
#使用cookie


#form={
#    'yes':'yes',
    #'from':'/bbs/Gossiping/index.html'
#    }

gossiping=r.post(over18_url)

#print(gossiping.text)
dom=BeautifulSoup(gossiping.text)
#print(dom)

#for title in (dom.find_all(class_='title')):
#    print(title.a['href'])

articleList=[]

for title in (dom.find_all(class_='title')):
    try:
        articleList.append(title.a['href'])
    except TypeError:
        continue
#print(articleList)

for article in articleList:
    root='https://www.ptt.cc/ask/over18?from='
    articleText=r.post(root+article,data=form).text
    articleDom=BeautifulSoup(articleText)
    outfile=open(article.replace('/bbs/Gossiping/','')+'.txt','w')
    print(articleDom)
   
    
    for content in articleDom.find( id='main-content').contents:
        try:
            outfile.write(content.text)
        except AttributeError:
            outfile.write(content)
    time.sleep(1)
