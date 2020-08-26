#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/7/29 16:58
'''
import datetime
import time
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from bs4 import BeautifulSoup

import Config

array = ['news_sina', 'news_eastmoney', 'news_10jqka', 'news_yuncaijing']
values = ['新浪', '东方财富', '同花顺', '云财经']
sources = dict(zip(array, values))


def getUrl(source):
    return f"https://tushare.pro/news/{source}"


def start_main(source):
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} StockIndexesMainSh.py  start")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Cookie":
            "session-id=e9262f2f-08f1-4d68-8fff-5d9570eaba71; uid=2|1:0|10:1597715034|3:uid|8:MzgzNzU0|0aae2d72db99d627aea63a21a714a6832cb4ef65fc939e3aa98bf42148cd6158; username=2|1:0|10:1597715034|8:username|16:MTg2ICoqKiAwMjc=|b6134806caf9a301e29c3dd26d6d675d335047310bf92149470a497e253477fa",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    data = requests.get(getUrl(source), headers=headers)
    content = data.content
    soup = BeautifulSoup(content, 'lxml')
    [s.extract() for s in soup.findAll('script')]
    values_array = []
    news_item = soup.find_all(class_="news_item")
    print(f"【start_main().soup={soup}】")
    dest_info = {}
    predate = datetime.date.today().strftime('%Y-%m-%d')
    for item in news_item:
        find = item.find(class_="news_datetime")
        if find:
            dest_info['news_source'] = sources[source]
            dest_info['news_date'] = f'{predate}'
            dest_info['news_hour'] = f'{find.text}'
            dest_info['news_content'] = item.find(class_="news_content").text
        else:
            predate = f"{getYesterday().year}-{item.text.replace('月', '-').replace('日', '')}"
            print(f"【start_main().predate============={predate}===============】")
        dest_info['type'] = "news_type"
        response = requests.post(Config.url, json=dest_info)
        print(f"insert {dest_info}{response.text}")
        values_array.append(dest_info)
        # print(f"【start_main().values_array={values_array}】")


def getYesterday():
    import datetime
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    return yesterday


def job_function():
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} TushareNews.py  start")
    for item in array:
        start_main(item)
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} TushareNews.py  end")

def login():
    pass

if __name__ == '__main__':
    job_function()
    # sched = BlockingScheduler()
    # sched.add_job(job_function, CronTrigger.from_crontab('0 9 * * *'))
    # sched.start()
