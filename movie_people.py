# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import random
import re
import requests
import os.path
from bs4 import BeautifulSoup
from pandas.core.frame import  DataFrame

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3346.8 Safari/537.36'
    }

def getListProxies():
    session = requests.session()
    page = session.get("http://www.xicidaili.com/nn", headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    proxyList = []
    taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
    for trtag in taglist:
        print len(proxyList)
        tdlist = trtag.find_all('td')
        proxy = {'http': tdlist[1].string + ':' + tdlist[2].string,
                 'https': tdlist[1].string + ':' + tdlist[2].string}
        url = "http://ip.chinaz.com/getip.aspx"  #用来测试IP是否可用的url
        try:
            response = session.get(url, proxies=proxy, timeout=5)
            proxyList.append(proxy)
            if(len(proxyList) == 4):
                break
        except Exception, e:
            continue

    return proxyList

proxy = getListProxies()
print proxy
ip = 0

def session1():
    global ip
    proxies = proxy[ip]
    ip = ip + 1
    ip = ip%4
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3346.8 Safari/537.36'
    }
    s = requests.session()
    try:
        r = s.get('https://movie.douban.com/', headers = headers, proxies = proxies)
    except Exception, e:
        session1()
    print proxies
    return s

def session2():
    try:
        s = session1()
    except Exception, e:
        s = session2()
    return s


user_name = list()
user_id = list()
user_movie = list()
user_pop = list()

movie_index = 26752852

for i in range(1,10+1):
    start = (i-1)*20
    page_comment = 'https://movie.douban.com/subject/' + str(movie_index) + '/comments?start=' + str(start)

    scrape_sleep = (1, 3, 4)

    s = session2()

    try:
        z = s.get(page_comment)
    except requests.exceptions.SSLError:
        time.sleep(random.sample(scrape_sleep, 1)[0])
        z = s.get(page_comment)

    page = z.text
    soup = BeautifulSoup(page,"html.parser")

    for j in range(0, 20):
        try:
            comment_info = soup.select('h3 > span.comment-info')[j]
        except IndexError:
            time.sleep(random.sample(scrape_sleep, 1)[0])
            comment_info = soup.select('h3 > span.comment-info')[j]

        people_url = comment_info.find('a')['href']
        user_id.append(re.findall(r'people/(.*?)/', people_url)[0])
        user_name.append(comment_info.find('a').text)

        try:
            people = BeautifulSoup((s.get(people_url)).text, "html.parser")
        except requests.exceptions.ConnectionError:
            time.sleep(random.sample(scrape_sleep, 1)[0])
            people = BeautifulSoup((s.get(people_url)).text, "html.parser")

        try:
            user_pop.append((re.findall(ur'\u88ab(\d+)', people.select('div.aside > p > a')[0].text))[0])
        except IndexError:
            user_pop.append('')
        try:
            user_movie.append((re.findall(r'(\d+)', people.select('div #movie > h2 > span > a')[-1].text))[0])
        except IndexError:
            user_movie.append('')

        print user_id
        print user_movie

        time.sleep(random.sample(scrape_sleep, 1)[0])

    current_dict = {
        "user_name": user_name,
        "user_id": user_id,
        "user_pop": user_pop,
        "user_movie": user_movie,
    }
    HH_dataframe = DataFrame(current_dict)
    HH_dataframe.to_csv('/Applications/学习/Google drive/暂放文件/SXWY_comment_people.csv')