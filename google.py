import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re


def google(q):
    # url="http://www.google.com/search?hl=en&q="+"+".join(GWord.split())
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
    searchGroup = []
    for i in output:
        searchResult = []
        str = i.find("a")['href'][7:]
        searchResult.append(re.match(pattern=r"(.+)&sa.+", string=str).group(1))
        searchResult.append(i.find("a").get_text())
        searchResult.append(i.find(class_="st").get_text())
        searchGroup.append(searchResult)
    return (searchGroup)
