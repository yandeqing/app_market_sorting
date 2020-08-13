#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/7/29 16:58
'''
import json
import random
import time

import requests
from bs4 import BeautifulSoup

import main


def getUrl(txtQueryDate):
    randomStr = float(random.randint(1, 100) / 1000000)
    return f"http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1803_sczm&TABKEY=tab1&txtQueryDate={txtQueryDate}&random={randomStr}"


def start_main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    strftime = time.strftime("%Y-%m-%d", time.localtime())
    data = requests.get(getUrl('2020-08-12'), headers=headers)
    content = data.json()[0]["data"]
    for item  in content:
        item['lbmc'] = item['lbmc'].replace('&nbsp;','')
        print(f"【start_main().response={item['lbmc']}】")
    dumps = json.dumps(content, ensure_ascii=False, indent=4)
    print(f"【start_main().response={dumps}】")
    # titles_array = []
    # values_array = []
    # table = soup.find_all(class_="table")[0]
    # childrens = table.findChildren('tr')
    # for children in childrens:
    #     find_childrens = children.findChildren('em')
    #     titles_childrens = children.findChildren('i')
    #     # print(f"【start_main().response={find_childrens}】")
    #     # print(f"【start_main().response={titles_childrens}】")
    #     values_array.extend([float(s.text) for s in find_childrens])
    #     titles_array.extend([s.text for s in titles_childrens])
    # dest = dict(zip(titles_array, values_array))
    # try:
    #     update_date = soup.find(class_='sse_home_in_table2').findChildren('span')[0].text
    #     print(f"【start_main().response={update_date}】")
    #     dest['update_date'] = update_date
    # except:
    #     pass
    # dest['type'] = 'stock_indexes'
    # print(f"【start_main().response={dest}】")
    # url = "http://139.129.229.205:8088"
    # response = requests.post(url, json=dest)
    # print(f"insert {dest}{response.text}")


if __name__ == '__main__':
    start_main()
