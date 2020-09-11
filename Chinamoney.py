#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/7/29 16:58
'''
import datetime
import random
import time

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import Config


def getUrl():
    return f"http://www.chinamoney.com.cn/ags/ms/cm-u-bond-publish/TicketHandle?t=1599623434436&t=1599623434437"

def start_main(strftime,type,insert_all=False):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    data = requests.get(getUrl(), headers=headers)
    print(f"requests {getUrl()}")
    content = data.json()["data"]["resultList"]
    for item in content:
        for key in item.keys():
            try:
                item[key] = trim(item[key])
            except:
               pass
        item['type'] = type
        item['update_date'] = strftime
        if item['operationFromDate']==strftime or insert_all:
            response = requests.post(Config.url, json=item)
            print(f"insert {item}{response.text}")


def trim(item):
    return float(item.replace(',', '')) if item.strip() else 0




def job_function():
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} Chinamoney.py  start")
    date = datetime.date.today().strftime('%Y-%m-%d')
    print(f"【main().date={date}】")
    start_main(date,"chinamoney_data",insert_all=False)
    print(f"{strftime} Chinamoney.py  end")





if __name__ == '__main__':
    job_function()
    # sched = BlockingScheduler()
    # sched.add_job(job_function, CronTrigger.from_crontab('21 9 * * *'))
    # sched.start()
