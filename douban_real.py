# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from bs4 import BeautifulSoup
import re
import urllib
import time
import random
from pandas.core.frame import  DataFrame
import csv

#现在还不知道一个账号访问过多会不会被封，先尝试一下

#登录函数

def login1():
    loginurl = 'https://accounts.douban.com/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3346.8 Safari/537.36'
    }
    formdata = {
        'source': 'None',
        'form_email': 'lliang37@wisc.edu',
        'form_password': 'Liangluwei1996886',
        'login': '登录'
    }
    z = requests.post(url = loginurl,data = formdata, headers = headers)
    page = z.text
    soup = BeautifulSoup(page, "html.parser")
    captchaAddr = soup.find('img', id='captcha_image')['src']
    reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
    captchaID = re.findall(reCaptchaID, page)
    urllib.urlretrieve(captchaAddr, "/Applications/学习/Google drive/暂放文件/captcha.jpg")
    captcha = raw_input('please input the captcha:')
    formdata['captcha-solution'] = captcha
    formdata['captcha-id'] = captchaID

    #构建login session, 传递cookie
    s= requests.session()
    r = s.post(loginurl, data=formdata, headers=headers)
    return s

#账号登录
def login2():
    loginurl = 'https://accounts.douban.com/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3346.8 Safari/537.36'
    }
    formdata = {
        'source': 'None',
        'form_email': 'lliang37@wisc.edu',
        'form_password': 'Liangluwei1996886',
        'login': '登录'
    }
    s= requests.session()
    r = s.post(loginurl, data=formdata, headers=headers)

    #检验账号是否登录成功
    if ('error') in r.url:
        s = login1()

    return s

s = login2()

#登录完毕，session构建成功

#利用同一session，遍历电影评价页，获得用户信息

#首先构建空列表，用以收集各式用户
user_id = list()
user_comment = list()
user_location = list()
user_time = list()
user_same = list()
user_pop = list()
user_movie = list()
user_book = list()
user_music = list()

#大循环，得到25个评论页面(登录后豆瓣也只显示短评的500个用户)
for i in range(1,25+1):
    #获取页面：
    start = (i-1)*20
    page_comment = 'https://movie.douban.com/subject/1292215/comments?start=' + str(start)

    #进入并解析页面：
    try:
        z = s.get(page_comment)
    except requests.exceptions.SSLError:
        time.sleep(5)
        z = s.get(page_comment)
    page = z.text
    soup = BeautifulSoup(page, "html.parser")

    #小循环，分别获得每一个评论界面上的20个用户(url，id，评分):
    for j in range(0,20):
        #首先抓取用户评论模块:
        comment_info = soup.select('h3 > span.comment-info')[j]
        people_url = comment_info.find('a')['href']
        user_id.append(comment_info.find('a').text)
        try:
            user_comment.append(re.findall(r'(\d+)', comment_info.findAll('span')[1]['class'][0])[0])
        except IndexError:
            user_comment.append('')

        #现在我们得到了用户在评论页的信息，接着进入用户页获取用户信息
        try:
            people = BeautifulSoup((s.get(people_url)).text, "html.parser")
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            people = BeautifulSoup((s.get(people_url)).text, "html.parser")
        try:
            user_info = people.select('div .user-info')[0]
        except IndexError:
            pass
        try:
            user_location.append(user_info.find('a').text)
        except AttributeError:
            user_location.append('')
        except IndexError:
            user_location.append('')
        try:
            user_time.append((re.findall(r'\s+(\d+-\d+-\d+)',user_info.find('div', class_= 'pl').text))[0])
        except IndexError:
            user_time.append('')
        try:
            user_same.append((re.findall(r'\((\d+)\)', (people.select('div #common')[0]).find('h2').text))[0])
        except IndexError:
            user_same.append('')
        try:
            user_pop.append((re.findall(ur'\u88ab(\d+)', people.select('div.aside > p > a')[0].text))[0])
        except IndexError:
            user_pop.append('')
        try:
            user_movie.append((re.findall(r'(\d+)', people.select('div #movie > h2 > span > a')[-1].text))[0])
        except IndexError:
            user_movie.append('')
        try:
            user_book.append((re.findall(r'(\d+)', people.select('div #book > h2 > span > a')[-1].text))[0])
        except IndexError:
            user_book.append('')
        try:
            user_music.append((re.findall(r'(\d+)', people.select('div #music > h2 > span > a')[-1].text))[0])
        except IndexError:
            user_music.append('')
        print user_id
        print user_comment
        print user_location
        print user_same
        print user_pop
        print user_movie

        people_sleep = (1, 3, 4, 6, 7)
        time.sleep(random.sample(people_sleep, 1)[0])

    current_dict = {
        "user_id" : user_id,
        "user_comment" : user_comment,
        "user_location" : user_location,
        "user_time" : user_time,
        "user_same" : user_same,
        "user_pop" : user_pop,
        "user_movie" : user_movie,
        "user_book" : user_book,
        "user_music" : user_music
    }
    HH_dataframe = DataFrame(current_dict)
    HH_dataframe.to_csv('/Applications/学习/Google drive/暂放文件/AML1.csv')

    sleep_bucket = (100, 151, 200, 201, 300, 301)

    if (len(user_id) >= 100) and (len(user_id) < 120):
        print '中间点, 休息5分钟'
        time.sleep(random.sample(sleep_bucket, 1)[0])
        s = login2()


    if (len(user_id) >= 200) and (len(user_id) < 220):
        print '中间点, 休息5分钟'
        time.sleep(random.sample(sleep_bucket, 1)[0])
        s = login2()

    if (len(user_id) >= 300) and (len(user_id) < 320):
        print '中间点, 休息5分钟'
        time.sleep(random.sample(sleep_bucket, 1)[0])
        s = login2()

    if (len(user_id) >= 400) and (len(user_id) < 420):
        print '中间点, 休息5分钟'
        time.sleep(random.sample(sleep_bucket, 1)[0])
        s = login2()