#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/7/29 16:58
'''
import json
import time

import requests
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
    try:
        update_date = soup.find(class_='sse_home_in_table2').findChildren('span')[0].text
        print(f"【start_main().response={update_date}】")
        dest['update_date'] = update_date
    except:
        pass
    dest['type'] = 'stock_indexes'
    print(f"【start_main().response={dest}】")
    url = "http://139.129.229.205:8088"
    response = requests.post(url, json=dest)
    print(f"insert {dest}{response.text}")


if __name__ == '__main__':
    start_main()
