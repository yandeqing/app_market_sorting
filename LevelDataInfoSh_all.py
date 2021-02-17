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
import data_uploader_helper


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


def getYesterday():
    import datetime
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    return yesterday


def getUrl(detailsDate, pageNo):
    return f"http://query.sse.com.cn/marketdata/tradedata/queryMargin.do?jsonCallBack=jsonpCallback47649&isPagination=true&tabType=mxtype&detailsDate={detailsDate}&stockCode=&beginDate=&endDate=&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo={pageNo}&pageHelp.beginPage={pageNo}&pageHelp.cacheSize=1&pageHelp.endPage=6&_=1600223819691"


def start_main(detailsDate):
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

    pageCount = 1
    pageNo = 0
    while pageNo < pageCount:
        time.sleep(0.5)
        pageNo = pageNo + 1
        url = getUrl(detailsDate, pageNo)
        print(f"【start_main().jsonp={url}】")
        data = requests.get(url, headers=headers)
        jsonp = loads_jsonp(data.text)
        results = jsonp['result']
        pageCount = jsonp['pageHelp']['pageCount']
        dest_info = {}
        for item in results:
            # print(f"insert {item}")
            dest_info['type'] = 'level_data_info'
            # if product_type != '43' and product_type!='40':
            dest_info['融券余量(万股/万份)'] = trim4(item['rqyl'])
            dest_info['融券余额(万元)'] = trim4(item['rqylje'])
            dest_info['融券卖出量(万股/万份)'] = trim4(item['rqmcl'])
            dest_info['融资买入额(亿元)'] = trim9(item['rzmre'])
            dest_info['融资余额(亿元)'] = trim9(item['rzye'])
            dest_info['融资融券余额(亿元)'] = trim9(item['rzrqjyzl'])
            dest_info['证券简称'] = item['securityAbbr']
            dest_info['证券代码'] = item['stockCode']
            dest_info['update_date'] = datetime.strptime(item['opDate'], "%Y%m%d").strftime(
                "%Y-%m-%d")
            dest_info['source'] = 'shanghai'
            # dest_info['pageNo'] = pageNo
            print(f"insert {json.dumps(dest_info, indent=4, ensure_ascii=False)}")
            response = requests.post(Config.url, json=dest_info, headers={'Connection': 'close'})
            print(f"insert {dest_info}{response.text}")



def trim9(item):
    try:
        return float(item / 100000000)
    except:
        return 0


def trim4(item):
    try:
        return float(item / 10000)
    except:
        return 0


def trim1(item):
    return float(item / 10000)


def job_function():
    if data_uploader_helper.is_trade_day():
        strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{strftime} LevelDataInfoSh_sum.py  start")
        date = getYesterday()
        print(f"【main().beginDate={date.strftime('%Y%m%d')}】")
        start_main(date.strftime('%Y%m%d'))
        strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{strftime} LevelDataInfoSh_sum.py  end")


def getDates(days):
    import datetime
    import time
    begin_date = (getYesterday()- datetime.timedelta(days=days)).strftime("%Y-%m-%d")
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
    # dates = getDates(10)
    # print(f"【().dates={dates}】")
    # for date in dates:
    #     start_main(date.replace("-",""))

    # job_function()
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('40 11 * * *'))
    sched.start()
