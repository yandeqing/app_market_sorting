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
    soup = BeautifulSoup(content, 'html.parser')
    [s.extract() for s in soup.findAll('script')]
    pagers = soup.find_all(class_="table")
    for table in pagers:
        childrens = table.findChildren('tr')
        for children in childrens:
            print(f"【start_main().response={children.findChildren('em')}】")


if __name__ == '__main__':
    start_main()
