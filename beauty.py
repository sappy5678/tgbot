# coding=UTF-8
from urllib import request
from bs4 import  BeautifulSoup
import re
import time
import sqlite3
import requests

def UpdateBeauty():
    r = requests.Session()
    print("start")
    root="https://www.ptt.cc"
    beauty="https://www.ptt.cc/bbs/Beauty/index.html"

    #respond=request.urlopen(beauty).read()
    respond=r.post(beauty).text
    respond=BeautifulSoup(respond, "html.parser")
    page=respond.find_all(class_="btn wide")
    page=int(re.search(pattern=".*index(.*).html",string=page[1]['href']).group(1))

    #sql 查詢
    conn = sqlite3.connect('DB/beauty.db')
    curs = conn.cursor()
    try:
        curs.execute('''create table beauty (id integer primary key, link text UNIQUE,tag text)''')
        params=('https://www.ptt.cc/bbs/Beauty/index1.html',)
        curs.execute("insert into beauty(link, tag) VALUES(?, 'preSotre')",params)
        conn.commit()
    except:
        print("start")

    curs.execute("select * from beauty where id=1")
    preSotre=curs.fetchall()
    page=page


    #preSotre=open("beauty.txt","r").readline()
    preSotre=re.search(pattern=".*index(.*).html",string=preSotre[0][1]).group(1)
    page=page+1
    #開始撈資料
    for i in range(int(preSotre),int(page)):
        time.sleep(5)

        urlObj=[]
        b=requests.session()
        #beautyData=open("beautyData.txt","a")
        print("status crawel page"+str(i))

        #respond=request.urlopen("https://www.ptt.cc/bbs/Beauty/index"+str(i)+".html").read()
        respond=b.post("https://www.ptt.cc/bbs/Beauty/index"+str(i)+".html").text
        respond=BeautifulSoup(respond, "html.parser")


        for q in respond.find_all(class_="title"):
            try:
                if (re.search(pattern=r".*正妹(.*)",string=q.get_text())!=None):
                    urlObj.append(root+q.a['href'])
            except:
                continue
        imgList=[]
        for p in urlObj:
            k=requests.session()

            try:
                img=k.post(p).text
            except:
                print("be block, wait for reconnect ")

                time.sleep(60)
                img=request.urlopen(p).read()


            #爬裡面的圖片
            img=BeautifulSoup(img, "html.parser")
            img=img.find_all("a")
            for b in img:
                #if(re.search(pattern=".*imgur.*",string=b.get_text())!=None):
                if(re.search(pattern=".*\.(jpg|gif|png)",string=b.get_text(),flags=re.I)!=None):
                    imgList.append(b['href'])
                    #beautyData.write(b['href']+"\n")

                    try:
                        curs.execute("insert into beauty(link) values(?)",(b['href'],))
                    except:
                        continue
        params=('https://www.ptt.cc/bbs/Beauty/index'+str(i)+'.html',)
        curs.execute("UPDATE beauty SET link=? WHERE id=1",params)

        conn.commit()
    params=('https://www.ptt.cc/bbs/Beauty/index'+str(page)+'.html',)
    curs.execute("UPDATE beauty SET link=? WHERE id=1",params)
    conn.commit()
    print("finish")

#UpdateBeauty()
