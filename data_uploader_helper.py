#!/usr/bin/env python
# coding=utf-8
'''
@author: yandeqing
@date:  2020/7/29 16:58
'''
import time

import requests

import Config
import industry_moneyflow_eastmoney


def upload_one(dest_info, type):
    dest_info['type'] = type
    response = requests.post(Config.url, json=dest_info, headers={'Connection': 'close'})
    print(f"insert {dest_info}{response.text}")


def is_trade_day(debug=False):
    if debug:
        return True
    date = industry_moneyflow_eastmoney.get_latest_date()
    time_strftime = time.strftime("%Y-%m-%d", time.localtime())
    if date != time_strftime:
        print(f"今天{time_strftime}不是交易日")
    return date == time_strftime


if __name__ == '__main__':
    print(is_trade_day())
