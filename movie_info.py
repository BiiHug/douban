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
from collections import OrderedDict

movie_id = 3530403

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3346.8 Safari/537.36',
        'Cookie': "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
}

movie_url = 'https://movie.douban.com/subject/' + str(movie_id) + '/'
r = requests.get(movie_url, headers = headers)
index_page = r.text
soup = BeautifulSoup(index_page,"html.parser")

movie_name = soup.select('h1 > span')[0].text
movie_time = soup.select('h1 > span')[1].text

movie_director = re.findall('.*?/celebrity/(\d+?)/',str(soup.select('div#info > span > span.attrs')[0]))
movie_actor = re.findall('.*?/celebrity/(\d+?)/',str(soup.select('span.actor')[0]))

movie_type = soup.select('span[property="v:genre"]')
movie_type = [unicode(i) for i in movie_type]
movie_type = ''.join(movie_type)
movie_type = re.findall(ur'<span property="v:genre">(.*?)</span>',movie_type)

movie_country = re.findall(ur'制片国家/地区:</span> (.*?)<br/>',unicode(soup.select('div#info')[0]))[0]
movie_country = movie_country.split(' / ')

movie_imdb = re.findall(ur'IMDb链接:</span> <a href=.*?>(.*?)</a>',unicode(soup.select('div#info')[0]))[0]

imdb_url = 'http://www.imdb.com/title/' + movie_imdb + '/'
r_imdb = requests.get(imdb_url)
index_page_imdb = r_imdb.text
soup_imdb = BeautifulSoup(index_page_imdb,"html.parser")

movie_english_name = soup_imdb.select('h1[itemprop="name"]')[0].text
movie_image = str(soup_imdb.select('div.poster > a > img')[0]['src'])

movie_rating_score = float(soup.select('strong.ll.rating_num')[0].text)
movie_rating_sum = int(soup.select('div.rating_sum > a > span')[0].text)
movie_rating_dist = soup.select('div.ratings-on-weight > div > span.rating_per')
movie_rating_dist = [str(i) for i in movie_rating_dist]
movie_rating_dist = ''.join(movie_rating_dist)
movie_rating_dist = re.findall('<span class="rating_per">(.*?)</span>',movie_rating_dist)


current_dict = {
        'id': movie_id,
        'name': movie_name,
        'English_name':  movie_english_name,
        'time': movie_time,
    }
current_dict = OrderedDict(current_dict)


for i in range(0, len(movie_type)):
    name = 'type'+str(i+1)
    current_dict[name] = movie_type[i]

current_dict['score'] = movie_rating_score
current_dict['pop'] = movie_rating_sum

for i in range(0, 5):
    name = 'rating'+str(5-i)+'star'
    current_dict[name] = movie_rating_dist[i]

for i in range(0, len(movie_country)):
    name = 'country'+str(i+1)
    current_dict[name] = movie_country[i]

for i in range(0, len(movie_director)):
    name = 'director'+str(i+1)
    current_dict[name] = movie_director[i]

for i in range(0, len(movie_actor)):
    name = 'actor'+str(i+1)
    current_dict[name] = movie_actor[i]

current_dict['poster'] = movie_image

HH_dataframe = DataFrame(current_dict, index=[0])
HH_dataframe.to_csv('/Applications/学习/Python/git_douban/data/movie_info/Yuntu_people_inspect.csv')

