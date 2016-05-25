# coding=UTF-8
from urllib import request
from bs4 import  BeautifulSoup
import re
import time
import sqlite3
import requests,random

def UpdateKodomo():
    r = requests.Session()
    print("start")
    root="https://www.ptt.cc"
    kodomo="https://www.ptt.cc/bbs/kodomo/index.html"

    #respond=request.urlopen(beauty).read()
    respond=r.post(kodomo).text
    respond=BeautifulSoup(respond, "html.parser")
    page=respond.find_all(class_="btn wide")
    page=int(re.search(pattern=".*index(.*).html",string=page[1]['href']).group(1))

    #sql 查詢
    conn = sqlite3.connect('DB/kodomo.db')
    curs = conn.cursor()
    try:
        curs.execute('''create table kodomo (id integer primary key, link text UNIQUE,tag text)''')
        params=('https://www.ptt.cc/bbs/kodomo/index1.html',)
        curs.execute("insert into kodomo(link, tag) VALUES(?, 'preSotre')",params)
        conn.commit()
    except:
        print("start")

    curs.execute("select * from kodomo where id=1")
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
        respond=b.post("https://www.ptt.cc/bbs/kodomo/index"+str(i)+".html").text
        respond=BeautifulSoup(respond, "html.parser")


        for q in respond.find_all(class_="title"):
            try:
                
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
                        curs.execute("insert into kodomo(link) values(?)",(b['href'],))
                    except:
                        continue
        params=('https://www.ptt.cc/bbs/kodomo/index'+str(i)+'.html',)
        curs.execute("UPDATE kodomo SET link=? WHERE id=1",params)

        conn.commit()
    params=('https://www.ptt.cc/bbs/kodomo/index'+str(page)+'.html',)
    curs.execute("UPDATE kodomo SET link=? WHERE id=1",params)
    conn.commit()
    print("finish")

#UpdateBeauty()

def kodomo(bot, update):
    if(update['message']['from_user']['username']!='sappy5678' and update['message']['from_user']['username']!='kaiyeee'):
        bot.sendMessage(update.message.chat_id, text="sorry you don't have the authority")
        return
    conn = sqlite3.connect('DB/kodomo.db')
    curs = conn.cursor()
    imgList=[]
    #i=0
    #while(i<=10):
    #    imgList.append(Data.readline())
    #Data.readline()
    #curs.execute("select top 100 link from beauty order by id desc")
    curs.execute("select link,id from kodomo where id>1")
    temp=curs.fetchall()
    #temp = [line[:-1] for line in imgList]
    img=random.choice(temp)
    flag=False



    while(flag==False):
        try:
            #bot.sendPhoto(update.message.chat_id, "http://imgur.com/a/91rUR")
            bot.sendPhoto(update.message.chat_id,img[0])
            flag=True
            #print("ppt")
            #bot.sendPhoto(update.message.chat_id,"http://ppt.cc/1ArC")
            #print("imgur")
            #bot.sendPhoto(update.message.chat_id,"http://imgur.com/c3PKEqI")
        except:
            #bot.sendMessage(update.message.chat_id, text=img[0])
            print('I am sorry about that,The image can\'t use')

            curs.execute("DELETE FROM kodomo WHERE id=?", (img[1],))
            conn.commit()


            img=random.choice(temp)
            print("delete img")