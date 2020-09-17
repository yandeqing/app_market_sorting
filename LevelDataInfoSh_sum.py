#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/7/29 16:58
'''
import json
import re
import time
from datetime import datetime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import Config


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


def getYesterday():
    import datetime
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    return yesterday


def getUrl(beginDate, endDate):
    return f"http://query.sse.com.cn/marketdata/tradedata/queryMargin.do?jsonCallBack=jsonpCallback45309&isPagination=true&beginDate={beginDate}&endDate={endDate}&tabType=&stockCode=&pageHelp.pageSize=25&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1600158718469"


def start_main(beginDate, endDate):
    dest_info = {}
    headers = {
        'Host': 'query.sse.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': 'http://www.sse.com.cn/market/othersdata/margin/detail/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
    url = getUrl(beginDate, endDate)
    print(f"【start_main().jsonp={url}】")
    data = requests.get(url, headers=headers)
    results = loads_jsonp(data.text)['result']
    dest_info = {}
    for item in results:
        dest_info['type'] = 'level_data_info_sum'
        # if product_type != '43' and product_type!='40':
        dest_info['融券余量(亿股/亿份)'] = trim(item['rqyl'])
        dest_info['融券余额(亿元)'] = trim(item['rqylje'])
        dest_info['融券卖出量(亿股/亿份)'] = trim(item['rqmcl'])
        dest_info['融资买入额(亿元)'] = trim(item['rzmre'])
        dest_info['融资余额(亿元)'] = trim(item['rzye'])
        dest_info['融资融券余额(亿元)'] = trim(item['rzrqjyzl'])
        dest_info['update_date'] = datetime.strptime(item['opDate'], "%Y%m%d").strftime("%Y-%m-%d")
        dest_info['source'] = 'shanghai'
        # print(f"insert {dest_info}")
        response = requests.post(Config.url, json=dest_info, headers={'Connection': 'close'})
        print(f"insert {dest_info}{response.text}")


def trim(item):
    return float(item / 100000000)


def trim1(item):
    return float(item / 10000)


def job_function():
    import datetime
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} LevelDataInfoSh_sum.py  start")
    date = getYesterday()
    if debug:
        date = datetime.date.today() + datetime.timedelta(-30)
    today_strftime = datetime.date.today().strftime('%Y%m%d')
    print(f"【main().beginDate={date.strftime('%Y%m%d')}】")
    print(f"【main().endDate={today_strftime}】")
    start_main(date.strftime('%Y%m%d'), today_strftime)
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} LevelDataInfoSh_sum.py  end")


#
debug = False
if __name__ == '__main__':
    # job_function()
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('50 9 * * *'))
    sched.start()
