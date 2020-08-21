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

array = ['GE', '00,20', '30', 'GE,30,00,20']
values = ['创业板', '主板', '中小企业板', '全部']
sources = dict(zip(array, values))


def getUrl(txtQueryDate, selectModule='GE,30,00,20'):
    randomStr = float(random.randint(1, 100) / 1000000)
    return f"http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1805_zb1&TABKEY=SYL&selectModule={selectModule}&txtDqrq={txtQueryDate}&random={randomStr}"


def start_main(strftime, selectModule):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    data = requests.get(getUrl(strftime, selectModule), headers=headers)
    print(f"requests {getUrl(strftime, selectModule)}")
    cols = data.json()[0]["metadata"]["cols"]
    content = data.json()[0]["data"]
    dests = []
    for item in content:
        dest = {}
        for key in item.keys():
            replace = cols[key].replace('<br>', '').replace('&nbsp;','')
            try:
                dest[replace] = trim(item[key])
            except:
                if '平均' in replace:
                    dest[replace] = 0
                else:
                    dest[replace] = item[key]
                pass
        dests.append(dest)
        dest['type'] = 'good_data_info'
        dest['select_mode'] = sources[selectModule]
        dest['update_date'] = strftime
        url = "http://139.129.229.205:8088"
        response = requests.post(url, json=dest)
        print(f"insert {dest}{response.text}")


def trim(item):
    print(f"trim={item}")
    return float(item.replace(',', '')) if item.strip() else 0


def getYesterday():
    import datetime
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    return yesterday


def job_function():
    date = getYesterday().strftime('%Y-%m-%d')
    print(f"【main().date={date}】")
    for mode in array:
        start_main(date, mode)
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} GoodDataInfo.py  end")


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


if __name__ == '__main__':
    # dates = getDates()
    # print(f"【().dates={dates}】")
    # for item in dates:
    #     for mode in array:
    #         start_main(item, mode)
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} GoodDataInfo.py  start")
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('20 10 * * *'))
    sched.start()
