from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import random
import sqlite3
from beauty import UpdateBeauty
import os


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Yes Master, what can I do for you?')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='This is the command list:')
    bot.sendMessage(update.message.chat_id, text='/start')
    bot.sendMessage(update.message.chat_id, text='/help')

def updateBeauty(bot, update):
    bot.sendMessage(update.message.chat_id, text='start to update database')
    try:
        UpdateBeauty()
    except:
        bot.sendMessage(update.message.chat_id, text='I am sorry, but my ip is ban, please wait and try it again')
        return
    bot.sendMessage(update.message.chat_id, text='update beauty finish')
def sing(bot, update):
    bot.sendMessage(update.message.chat_id, text='Send them to the slguhterhouse')
    bot.sendMessage(update.message.chat_id, text='Breeeeeeeeeeeeeeeee')

def beauty(bot, update):
    conn = sqlite3.connect('DB/beauty.db')
    curs = conn.cursor()
    #Data=open("beautyData.txt","r")
    imgList=[]
    #i=0
    #while(i<=10):
    #    imgList.append(Data.readline())
    #Data.readline()
    #curs.execute("select top 100 link from beauty order by id desc")
    curs.execute("select link,id from beauty where id>1")
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

            curs.execute("DELETE FROM beauty WHERE id=?", (img[1],))
            conn.commit()


            img=random.choice(temp)
            print("delete img")




def photoTest(bot,update):
    bot.sendPhoto(update.message.chat_id,"http://static.ettoday.net/images/1387/d1387895.jpg")
    bot.sendVideo(update.message.chat_id,"https://youtu.be/K7E3Aw4brMM")


def handsome(bot,update):
    bot.sendMessage(update.message.chat_id, text='sappy5678 is a handsome boy www')

   #  print(Filters.text[1])
def google(bot,update):
    print(update.message.text[8:])
    q=update.message.text[8:]
    url = "https://www.google.com.tw/search?q=" + q + "&start=0"

    req = urllib.request.Request(url)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML,     like Gecko) Chrome/0.2.149.29 Safari/525.13")

    content = urllib.request.urlopen(req).read()
    content = BeautifulSoup(content, "html.parser")
    # print(content)
    # output=content.find_all(attrs={"style":"font:smaller \'Doulos SIL\',\'Gentum\',\'TITUS Cyberbit Basic\',\'Junicode\',\'Aborigonal Serif\',\'Arial Unicode MS\',\'Lucida Sans Unicode\',\'Chrysanthi Unicode\';padding-left:15px"})
    # output=content.find("div",{"class":"srg"})
    output = content.find_all("div", attrs={"class", "g"})

    # 整理結果
    result = []
    for i in output:
        searchResult = []
        str = i.find("a")['href'][7:]
        searchResult.append(re.match(pattern=r"(.+)&sa.+", string=str).group(1))
        searchResult.append(i.find("a").get_text())
        searchResult.append(i.find(class_="st").get_text())
        result.append(searchResult)


    bot.sendMessage(update.message.chat_id, text=result[0][0]+" "+result[0][1])
def main():
    print("bot start")

    # pass the token
    # updater = Updater("118322299:AAGs7WMxAJCqKfS9CmUHE6X9SwGqtb3P6YM")
    key=os.environ['whitebot']
    updater = Updater(key)

    # dispatcher
    disp = updater.dispatcher

    disp.addHandler(CommandHandler("start", start))
    disp.addHandler(CommandHandler("help", help))
    disp.addHandler(CommandHandler("sing", sing))
    disp.addHandler(CommandHandler("photoTest",photoTest))
    disp.addHandler(CommandHandler("google",google))
    disp.addHandler(CommandHandler("beauty",beauty))
    disp.addHandler(CommandHandler("Ubeauty",updateBeauty))
    disp.addHandler(MessageHandler([Filters.text],handsome))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
        main()

