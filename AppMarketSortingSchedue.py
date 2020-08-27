#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/8/12 10:26
'''
import json
import time

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import Config


def getUrl(num):
    return f"https://wap1.hispace.hicloud.com/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum={num}" \
           "&uri=1ca1964fe0c343cbab12f94d6dc5ef7e&maxResults=25&zone=&locale=zh_CN"


def randomTime(a, b):
    import random
    randint = random.randint(a, b)
    return randint


def start_main():
    apps = []
    hasNextPage = 1
    page = 0
    while hasNextPage:
        random_time = randomTime(0, 10)
        print(f"【main().sleep={random_time}】")
        time.sleep(random_time)
        page += 1
        get = requests.get(url=getUrl(page), headers="", timeout=30)
        response = get.json()
        hasNextPage = response['hasNextPage']
        print(f"【main().page={page}】")
        obj = response['layoutData'][0]['dataList']
        for item in obj:
            app = {}
            app['type'] = 'app'
            app['name'] = item['name']
            app['tagName'] = item['tagName']
            downCountDesc = item['downCountDesc'].replace(' ', '').replace(',', '')
            app['downCountDesc'] = item['downCountDesc']
            if '万次安装' in downCountDesc:
                replace = downCountDesc.replace('万次安装', '')
                dowloadCount = float(replace) / 10000
                app['dowloadCount'] = dowloadCount
            elif '亿次安装' in downCountDesc:
                replace = downCountDesc.replace('亿次安装', '')
                dowloadCount = float(replace)
                app['dowloadCount'] = dowloadCount
            elif '次安装' in downCountDesc:
                replace = downCountDesc.replace('次安装', '')
                dowloadCount = float(replace)
                app['dowloadCount'] = dowloadCount
            app['createTime'] = time.strftime('%Y-%m-%d', time.localtime())
            apps.append(app)
    dumps = json.dumps(apps, ensure_ascii=False, indent=4)
    # classFy = [app for app in apps if app['tagName'] == '股票基金']
    # dumps = json.dumps(classFy, ensure_ascii=False, indent=4)
    print(f"【main().json={dumps}】")
    for app in apps:
        insert(app)


def insert(payload):
    # payload = {
    #     "type": "app",
    #     "name": "39. 同花顺",
    #     "tagName": "股票基金",
    #     "downCountDesc": "4亿次安装",
    #     "dowloadCount": 4.0,
    #     "createTime": "2020-07-30"
    # }
    response = requests.post(Config.url, json=payload)
    print(f"insert {payload}{response.text}")

def job_function():
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} AppMarketSortingSchedue.py  start")
    start_main()
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} AppMarketSortingSchedue.py  end")

if __name__ == '__main__':
    job_function()
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('30 19 * * *'))
    sched.start()
