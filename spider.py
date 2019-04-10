#!/usr/bin/env python
#file domain.py
# coding: utf8 

import requests
from bs4 import BeautifulSoup

def getURL():
    for i in range(1, 77):
        url = "https://infodoanhnghiep.com/Quang-Nam/Thanh-pho-Hoi-An/trang-" + str(i) + "/"
        print(url)
        result = requests.get(url)
        soup = BeautifulSoup(str(result.content), "html.parser")
        # find all div that has class = "company-item"
        divs = soup.find_all("div")
        for div in divs:
            if("class" in div.attrs):
                for divProperty in div.attrs["class"]:
                    if(str(divProperty) == "company-item"):
                        getHREF(div)


def writeToFile(fileName, data):
    file = open(fileName, "a")
    file.write(data);
    file.close();

def getHREF(father):
    aTagList = father.find_all("a")
    for aTag in aTagList:
        if aTag.get("href") is not None:
            writeToFile("url_list/urls", "https:" + aTag.get('href') + "\n")

def getCompanyInfo(url):
    result = requests.get(url)
    soup = BeautifulSoup(str(result.content), "html.parser")
    # get div that contains company info
    divTagList = soup.find_all("div")
    for div in divTagList:
        if ("class" in div.attrs):
            allClass = ' '.join(div.attrs["class"])
            if (allClass == "responsive-table responsive-table-2cols responsive-table-collapse"): # that div contains company info
                getDivContent(div)

def getDivContent(father):
    divChildList = father.find_all("div")
    flag = 0
    text = ""
    with open("headers", "r") as fp:
        header = fp.readline()
        while header:
            for div in divChildList:
                divContent = div.getText().encode("utf-8").strip()
                if (flag == 1):
                    text += "\"" + div.getText() + "\"" + ","
                    flag = 0
                if(divContent.strip() == header.strip()):
                    flag = 1
            header = fp.readline()
            
    text = text.encode("utf-8").strip()
    writeToFile("infos.csv", text[:-1] + "\n")

def start():
    with open("url_list/urls", "r") as fp:
        url = fp.readline()
        while url:
            print(url)
            getCompanyInfo(url)
            url = fp.readline()

start()

