# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from bs4 import BeautifulSoup
import re
import os.path
import json

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3346.8 Safari/537.36'
    }

file = open('/Applications/学习/Python/git_douban/douban/proxyList.json','r')
proxyList = json.load(file)

def check_proxy(proxyList):
    proxyList2 = []
    for proxy in proxyList:
        print len(proxyList2)
        url = "http://www.baidu.com/"
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            if (response.url == url) and (int(len(response.headers)) >= 2):
                proxyList2.append(proxy)
            if (len(proxyList2) == 100):
                break
        except Exception, e:
            print e
            continue

    print len(proxyList2)

    proxyList3 = []
    for proxy in proxyList2:
        print len(proxyList3)
        url = "http://www.baidu.com/"
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            if (response.url == url) and (int(len(response.headers)) >= 3):
                proxyList3.append(proxy)
            if (len(proxyList3) == 100):
                break
        except Exception, e:
            print e
            continue
    print len(proxyList3)

    return proxyList3

proxyList3 = check_proxy(proxyList)

j = 1
def ip_supply(proxyList3):
    global j
    for i in range(j, 1001):
        print j
        print i
        session = requests.session()
        page = session.get("http://www.xicidaili.com/nn/" + str(i), headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
        for trtag in taglist:
            if trtag not in proxyList3:
                print len(proxyList3)
                tdlist = trtag.find_all('td')
                proxy = {'http': tdlist[1].string + ':' + tdlist[2].string,
                         'https': tdlist[1].string + ':' + tdlist[2].string}
                url = "http://www.baidu.com/"  # 用来测试IP是否可用的url
                try:
                    response = session.get(url, proxies=proxy, timeout=3)
                    if (response.url == url) and (int(len(response.headers)) >= 2):
                        proxyList3.append(proxy)
                    if (len(proxyList3) == 10):
                        break
                except Exception, e:
                    print e
                    continue
        if (len(proxyList3) == 10):
            break
        print len(proxyList3)
        j = j+1
    return proxyList3

while len(proxyList3) <6:
    proxyList3 = ip_supply(proxyList3)
    proxyList3 = check_proxy(proxyList3)

js_proxy = json.dumps(proxyList3)
filejs = open('/Applications/学习/Python/git_douban/douban/proxyList.json','w')
filejs.write(js_proxy)
filejs.close()