#!/usr/bin/env python
# coding=utf-8
'''
@author: yandeqing
@date:  2020/7/29 16:58
'''
import requests

import Config
import industry_moneyflow_eastmoney


def upload_one(dest_info, type):
    dest_info['type'] = type
    response = requests.post(Config.url, json=dest_info, headers={'Connection': 'close'})
    print(f"insert {dest_info}{response.text}")

if __name__ == '__main__':
    print(industry_moneyflow_eastmoney.get_latest_date())