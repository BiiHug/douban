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

user_id = 62445798

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3346.8 Safari/537.36',
        'Cookie': "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
}

#先进入第一页，以寻找总页数
collect_url = 'https://movie.douban.com/people/' + str(user_id) + '/collect'
r = requests.get(collect_url, headers = headers)
index_page = r.text
soup = BeautifulSoup(index_page,"html.parser")

#总页数找到
page_num = int(soup.select('div.paginator > span.thispage')[0]['data-total-page'])

#初始化
movie_id_list = []
movie_score_list = []
movie_time_list = []
movie_comment_list = []

page_ul = soup.select('div.item > div.info > ul')

for item_ul in page_ul:
    try:
        movie_id_list.append(int(re.findall('.*?/subject/(\d+)/' , item_ul.select('li.title > a')[0]['href'])[0]))
    except IndexError:
        movie_id_list.append('')
    try:
        movie_score_list.append(int(re.findall('rating(\d)-t',str(item_ul.findAll('span')))[0]))
    except IndexError:
        movie_score_list.append('')
    try:
        movie_time_list.append(item_ul.select('li > span.date')[0].text)
    except IndexError:
        movie_time_list.append('')
    try:
        movie_comment_list.append(item_ul.select('li > span.comment')[0].text)
    except IndexError:
        movie_comment_list.append('')
    print movie_score_list

for i in range(2,page_num+1):
    print i
    collect_url = 'https://movie.douban.com/people/' + str(user_id) + '/collect?start=' + str((i-1)*15)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3346.8 Safari/537.36',
        'Cookie': "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
    }
    try:
        r = requests.get(collect_url, headers=headers, timeout=5)
    except Exception, e:
        time.sleep(3)
        r = requests.get(collect_url, headers=headers, timeout=5)
    index_page = r.text
    soup = BeautifulSoup(index_page, "html.parser")
    page_ul = soup.select('div.item > div.info > ul')
    for item_ul in page_ul:
        try:
            movie_id_list.append(int(re.findall('.*?/subject/(\d+)/', item_ul.select('li.title > a')[0]['href'])[0]))
        except IndexError:
            movie_id_list.append('')
        try:
            movie_score_list.append(int(re.findall('rating(\d)-t', str(item_ul.findAll('span')))[0]))
        except IndexError:
            movie_score_list.append('')
        try:
            movie_time_list.append(item_ul.select('li > span.date')[0].text)
        except IndexError:
            movie_time_list.append('')
        try:
            movie_comment_list.append(item_ul.select('li > span.comment')[0].text)
        except IndexError:
            movie_comment_list.append('')
    print movie_score_list

    current_dict = {
        "user_id": user_id
        "movie_id": movie_id_list,
        "movie_score": movie_score_list,
        "movie_time": movie_time_list,
        "movie_comment": movie_comment_list,
    }
    HH_dataframe = DataFrame(current_dict)
    HH_dataframe.to_csv('/Applications/学习/Python/git_douban/data/people_inspect/XXDS_people_inspect.csv')
    time.sleep(int(random.sample(range(0,5),1)[0]))