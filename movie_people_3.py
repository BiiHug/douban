# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import random
import re
import requests
import os.path
import string
from bs4 import BeautifulSoup
from pandas.core.frame import  DataFrame

movie_index = 5045678

Agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER', 
]

def request1(page_comment):
    headers1 = {
        'User-Agent': random.sample(Agent_list,1)[0],
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/subject/'+str(movie_index)+'/',
    }
    print headers1['User-Agent']
    r = requests.get(page_comment, headers = headers1)
    print r.headers['Set-Cookie']
    return r, headers1['User-Agent'], r.headers['Set-Cookie']

def session1(people_url, agent, cookie, page_comment):
    headers2 = {
        'User-Agent': agent,
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'www.douban.com',
        'Referer': page_comment,
        'Cookie': cookie
    }
    s = requests.session()
    r = s.get(people_url, headers = headers2)
    print r.headers
    return s

user_name = list()
user_id = list()
user_movie = list()
user_pop = list()


for i in range(1,10+1):
    start = (i-1)*20
    page_comment = 'https://movie.douban.com/subject/' + str(movie_index) + '/comments?start=' + str(start)

    scrape_sleep = (1, 3, 4, 5)

    r, agent, cookie = request1(page_comment)

    page = r.text
    soup = BeautifulSoup(page,"html.parser")

    comment_info = soup.select('h3 > span.comment-info')[0]
    people_url = comment_info.find('a')['href']
    s = session1(people_url,agent,cookie,page_comment)

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

        time.sleep(15)

    current_dict = {
        "user_name": user_name,
        "user_id": user_id,
        "user_pop": user_pop,
        "user_movie": user_movie,
    }
    HH_dataframe = DataFrame(current_dict)
    HH_dataframe.to_csv('/Applications/学习/Python/git_douban/data/comment_people/DYHT_comment_people.csv')