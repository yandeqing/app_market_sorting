#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/7/29 16:58
'''
import time
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from bs4 import BeautifulSoup


def getUrl():
    return f"http://www.sse.com.cn/market/stockdata/statistic/"


def start_main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    data = requests.get(getUrl(), headers=headers)
    content = data.content
    soup = BeautifulSoup(content, 'lxml')
    [s.extract() for s in soup.findAll('script')]
    titles_array = []
    values_array = []
    table = soup.find_all(class_="table")[0]
    childrens = table.findChildren('tr')
    for children in childrens:
        find_childrens = children.findChildren('em')
        titles_childrens = children.findChildren('i')
        # print(f"【start_main().response={find_childrens}】")
        # print(f"【start_main().response={titles_childrens}】")
        values_array.extend([float(s.text) for s in find_childrens])
        titles_array.extend([s.text for s in titles_childrens])
    dest = dict(zip(titles_array, values_array))
    dest_info = {}
    try:
        update_date = soup.find(class_='sse_home_in_table2').findChildren('span')[0].text
        print(f"【start_main().response={update_date}】")
        dest_info['update_date'] = update_date
    except:
        pass
    dest_info['type'] = 'sz_stock_indexes'
    dest_info['lbmc'] = '上证股票'
    dest_info['sjzz'] = dest['总市值/亿元']
    print(f"【start_main().response={dest_info}】")
    url = "http://139.129.229.205:8088"
    response = requests.post(url, json=dest_info)
    print(f"insert {dest_info}{response.text}")
    print(f"{strftime} StockIndexesMainSh.py  end")


if __name__ == '__main__':
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} StockIndexesMainSh.py  start")
    sched = BlockingScheduler()
    sched.add_job(start_main, CronTrigger.from_crontab('15 9 * * *'))
    sched.start()
