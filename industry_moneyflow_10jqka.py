import json
import re
import time

import pandas
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import Config
import data_uploader_helper
import industry_moneyflow_eastmoney
from chorme import chorme_base


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


def transfer_fields(item_source):
    # ['序号', '行业', '行业指数', '涨跌幅', '流入资金(亿)', '流出资金(亿)', '净额(亿)', '公司家数', '领涨股', '涨跌幅.1', '当前价(元)']
    item = {}
    item['板块名称'] = item_source.get('行业')
    item['净流入'] = item_source.get('净额(亿)')
    item['净流入占比'] = round(100 * item_source.get('净额(亿)') / (item_source.get('流入资金(亿)') + item_source.get('流出资金(亿)')), 2)
    item['板块指数值'] = item_source.get('行业指数')
    item['涨跌幅'] = item_source.get('涨跌幅.1').replace('%', '')
    return item


# 网页提取函数
def get_one_page(page):
    try:
        url = f'http://data.10jqka.com.cn/funds/hyzjl/field/tradezdf/order/desc/page/{page}/ajax/1/free/1/'
        print(f'url={url}')
        text = chorme_base.get_page_source(url)
        if text:
            return text
        # Host: data.10jqka.com.cn
        # User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0
        # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
        # Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
        # Accept-Encoding: gzip, deflate
        # Connection: keep-alive
        # Cookie: v=A3AYpovQ5FoufbheEVL1LP1WQT_CuVQDdp2oB2rBPEueJR5vEskkk8ateJa5; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1613274366; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1613301091; __utma=156575163.736018167.1613274416.1613274416.1613274416.1; __utmc=156575163; __utmz=156575163.1613274416.1.1.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1613300864; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1613301091; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1613300864; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1613301091
        # Upgrade-Insecure-Requests: 1
        # Pragma: no-cache
        # Cache-Control: no-cache
        header = {}
        header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        header['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
        header['Accept-Encoding'] = 'gzip, deflate'
        header['Upgrade-Insecure-Requests'] = '1'
        header['Connection'] = 'keep-alive'
        header['Pragma'] = 'no-cache'
        header['Cache-Control'] = 'no-cache'
        header[
            'Cookie'] = 'v=A9pL3pRPbrYUr-IaAwwXmp4kK4H8C17l0I_SieRThm04V3QhzJuu9aAfIpi3'
        header['Host'] = 'data.10jqka.com.cn'
        header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        print(f'爬取失败{e}')


def getdata(page):
    text = get_one_page(page)
    print(text)
    df = pandas.read_html(text, )[0]
    keys = df.keys()
    print(list(keys))
    new_item_arr = []
    for item in df.values:
        new_item = {}
        for index, subitem in enumerate(item):
            new_item[keys[index]] = subitem
        new_item_arr.append(new_item)
    return new_item_arr


def job_function():
    if data_uploader_helper.is_trade_day(True):
        date = industry_moneyflow_eastmoney.get_latest_date()
        print(date)
        new_item_arr = []
        for i in range(2):
            data = getdata(i + 1)
            new_item_arr.extend(data)
        for index,item in enumerate(new_item_arr):
            item = transfer_fields(item)
            item['source'] = '同花顺'
            item['交易日期'] = date
            print(f"insert {index}.{item}")
            data_uploader_helper.upload_one(item, 'industry_money_flow')
        dumps = json.dumps(new_item_arr, indent=4, ensure_ascii=False)
        print(dumps)


if __name__ == '__main__':
    job_function()
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('35 18 * * *'))
    sched.start()
    # getdata(2)
