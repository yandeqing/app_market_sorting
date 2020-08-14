#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/7/29 16:58
'''
import datetime
import json
import random
import time

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def getLast12Months():
    begin_date = 1
    reference_date = datetime.date.today()
    date_list = []
    while begin_date <= 12:
        date = getLastMonth(reference_date)
        date_list.append(date.strftime('%Y-%m'))
        reference_date = date
        begin_date += 1
    return date_list


def getUrl(txtQueryDate,pageno=1):
    randomStr = float(random.randint(1, 100) / 1000000)
    return f"http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1803_sczm&TABKEY=tab2&PAGENO={pageno}&DATETIME={txtQueryDate}&random={randomStr}"


def start_main(strftime,pageno=1):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    data = requests.get(getUrl(strftime,pageno), headers=headers)
    content = data.json()[1]['data']
    for item in content:
        del item['rowid']
        for key in item.keys():
            if key != 'dq':
                item[key] = trim(item[key])
        item['type'] = 'transaction_by_area'
        item['update_date'] = strftime+"-01"
        url = "http://139.129.229.205:8088"
        response = requests.post(url, json=item)
        print(f"insert {item}{response.text}")
    dumps = json.dumps(content, ensure_ascii=False, indent=4)
    print(f"【start_main().response={dumps}】")


def trim(item):
    print(f"trim={item}")
    return float(item.replace(',', '')) if item.strip() else 0


def job_function():
    date_today = datetime.date.today()
    date = getLastMonth(date_today).strftime('%Y-%m')
    print(f"【main().date={date}】")
    start_main(date,1)
    start_main(date,2)
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} StockIndexesMainSz.py  end")


def getLastMonth(reference_date):
    last_month = reference_date.replace(day=1) - datetime.timedelta(days=1)
    date = last_month
    return date


if __name__ == '__main__':
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} TransactionByArea.py  start")
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('17 9 1 * *'))
    sched.start()
