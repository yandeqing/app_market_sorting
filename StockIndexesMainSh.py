#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/7/29 16:58
'''
import json
import re
import time

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import Config


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


def getDayBeforeToday(n):
    import datetime
    yesterday = datetime.date.today() + datetime.timedelta(-n)
    return yesterday


def getUrl(searchDate):
    return f"http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback18700&searchDate={searchDate}&sqlId=COMMON_SSE_SJ_GPSJ_CJGK_DAYCJGK_C&stockType=90&_={int(time.time() * 1000)}"


def start_main(searchDate):
    dest_info = {}
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} StockIndexesMainSh.py  start")
    headers = {
        'Host': 'query.sse.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': 'http://www.sse.com.cn/market/stockdata/overview/day/',
        # 'Cookie': 'JSESSIONID=75F3327F6277F963CBFBDEF11E466AD1; yfx_c_g_u_id_10000042=_ck20090810012310712757532516914; yfx_f_l_v_t_10000042=f_t_1599530482942__r_t_1599530482942__v_t_1599530482942__r_c_0; VISITED_MENU=%5B%228451%22%2C%2211913%22%2C%228464%22%2C%228466%22%5D',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
    url = getUrl(searchDate)
    print(f"【start_main().jsonp={url}】")
    data = requests.get(url, headers=headers)
    results = loads_jsonp(data.text)['result']
    dest_info = {}
    for item in results:
        # dumps = json.dumps(item, indent=4, ensure_ascii=False)
        dest_info['type'] = 'sz_stock_indexes'
        product_type = item['PRODUCT_TYPE']
        if product_type != '43' and product_type!='40':
            dest_info['lbmc'] =getName(product_type)
            dest_info['sjzz'] =float(item['MKT_VALUE'])
            dest_info['zqsl'] = 0
            dest_info['update_date'] = searchDate
            dest_info['ltsz'] =float( item['NEGOTIABLE_VALUE'])
            response = requests.post(Config.url, json=dest_info, headers={'Connection': 'close'})
            print(f"insert {dest_info}{response.text}")

    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} StockIndexesMainSh.py  end")

def getName(product_type):
    if product_type=='1':
        return '上证主板A'
    if product_type=='2':
        return '上证主板B'
    if product_type=='12':
        return '上证股票'
    if product_type=='48':
        return '科创板'
    return product_type


def getDates(days):
    import datetime
    import time
    begin_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())),
                                          "%Y-%m-%d")
    while begin_date < end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list

def job_function():
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} StockIndexesMainSh.py  start")
    from datetime import datetime
    # dayOfWeek = datetime.now().isoweekday()
    # if dayOfWeek==1:
    #     date = getDayBeforeToday(3).strftime('%Y-%m-%d')
    # else:
    date = getDayBeforeToday(1).strftime('%Y-%m-%d')
    print(f"【main().date={date}】")
    start_main(date)
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} StockIndexesMainS.py  end")

if __name__ == '__main__':
    # dates = getDates(30)
    # print(f"【().dates={dates}】")
    # for item in dates:
    #     start_main(item)
    # job_function()
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('24 9 * * *'))
    sched.start()
