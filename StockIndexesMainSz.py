#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/7/29 16:58
'''
import random
import time

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def getDates():
    import datetime
    import time
    begin_date = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime("%Y-%m-%d")
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())),
                                          "%Y-%m-%d")
    while begin_date < end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def getUrl(txtQueryDate):
    randomStr = float(random.randint(1, 100) / 1000000)
    return f"http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1803_sczm&TABKEY=tab1&txtQueryDate={txtQueryDate}&random={randomStr}"


def start_main(strftime):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    data = requests.get(getUrl(strftime), headers=headers)
    content = data.json()[0]["data"]
    for item in content:
        item['type'] = 'sz_stock_indexes'
        item['lbmc'] = item['lbmc'].replace('&nbsp;', '')
        item['update_date'] = strftime
        item['zqsl'] = trim(item['zqsl'])
        item['cjje'] = trim(item['cjje'])
        item['cjsl'] = trim(item['cjsl'])
        item['zgb'] = trim(item['zgb'])
        item['sjzz'] = trim(item['sjzz'])
        item['ltgb'] = trim(item['ltgb'])
        item['ltsz'] = trim(item['ltsz'])
        print(f"【start_main().response={item}】")
        url = "http://139.129.229.205:8088"
        response = requests.post(url, json=item)
        print(f"insert {item}{response.text}")


def trim(item):
    return float(item.replace(',', '')) if item.strip() else 0


def getYesterday():
    import datetime
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    return yesterday

def job_function():
    date = getYesterday().strftime('%Y-%m-%d')
    print(f"【main().date={date}】")
    start_main(date)
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} StockIndexesMainSz.py  end")

if __name__ == '__main__':
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} StockIndexesMainSz.py  start")
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('47 9 * * *'))
    sched.start()

