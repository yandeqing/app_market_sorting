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

import Config



def getUrl(txtQueryDate, tab2PAGENO=1):
    randomStr = float(random.randint(1, 100) / 1000000)
    return f"http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1837_xxpl&tab2PAGENO={tab2PAGENO}&txtDate={txtQueryDate}&random={randomStr}"

def start_main(metaIndex,strftime, pageNo,type):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    data = requests.get(getUrl(strftime, pageNo), headers=headers)
    print(f"requests {getUrl(strftime, pageNo)}")

    cols = data.json()[metaIndex]["metadata"]["cols"]
    pagecount = data.json()[1]["metadata"]["pagecount"]
    content = data.json()[metaIndex]["data"]
    dests = []
    for item in content:
        dest = {}
        for key in item.keys():
            replace = cols[key].replace('<br>', '').replace('&nbsp;','')
            try:
                dest[replace] = trim(item[key])
            except:
                dest[replace] = item[key].strip().replace('&nbsp;','')
        dests.append(dest)
        dest['type'] = type
        dest['update_date'] = strftime
        response = requests.post(Config.url, json=dest)
        # print(f"insert {dest}")
        print(f"insert {dest}{response.text}")
        # time.sleep(1)
    return  pagecount


def trim(item):
    return float(item.replace(',', '')) if item.strip() else 0


def getYesterday():
    import datetime
    yesterday = datetime.date.today() + datetime.timedelta(-2)
    return yesterday


def job_function():
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} LevelDataInfo.py  start")
    date = getYesterday().strftime('%Y-%m-%d')
    print(f"【main().date={date}】")
    getDataByDate(date)


def getDataByDate(date):
    # 统计总数
    count = start_main(0, date, 1, "'level_data_info_sum'")
    for i in range(1, count):
        # 统计详情 个股
        start_main(1, date, i, "'level_data_info'")
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} LevelDataInfo.py  end")


def getDates():
    import datetime
    import time
    begin_date = (getYesterday() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())),
                                          "%Y-%m-%d")
    while begin_date < end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


if __name__ == '__main__':
    # dates = getDates()
    # print(f"【().dates={dates}】")
    # for item in dates:
    #     getDataByDate(item)
    job_function()
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('10 7 * * *'))
    sched.start()
