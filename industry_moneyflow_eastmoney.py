import json
import re
import time

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


def transfer_fields(item_source):
    item = {}
    item['板块名称'] = item_source.pop('f14')
    value = 0
    try:
        value = round(item_source.pop('f62') / (10000 * 10000), 2)
    except:
        pass
    item['净流入'] = value
    item['净流入占比'] = item_source.pop('f184')
    item['板块指数值'] = item_source.pop('f2')
    item['涨跌幅'] = item_source.pop('f3')
    time_strftime = time.strftime("%Y-%m-%d", time.localtime(item_source.pop('f124')))
    item['交易日期'] = time_strftime
    return item


def get_latest_date():
    url = 'http://push2.eastmoney.com/api/qt/clist/get'
    params = {}
    params['cb'] = 'callback'
    params['fid'] = 'f62'
    params['po'] = 1
    params['pz'] = 200
    params['pn'] = 1
    params['fltt'] = 2
    params['invt'] = 2
    params['ut'] = 'b2884a393a59ad64002292a3e90d46a5'
    params['fs'] = 'm:90 t:2'
    params['fields'] = 'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124'
    df = requests.get(url, params=params)
    jsonp = loads_jsonp(df.text)
    if jsonp:
        data = jsonp.get('data')
        diff = data.get('diff')
        total = data.get('total')
        print(f'total={total}')
        if total > 0:
            item_source = diff.get("0")
            time_strftime = time.strftime("%Y-%m-%d", time.localtime(item_source.get('f124')))
            print(time_strftime)
            return time_strftime


def get_industry():
    url = 'http://push2.eastmoney.com/api/qt/clist/get'
    params = {}
    params['cb'] = 'callback'
    params['fid'] = 'f62'
    params['po'] = 1
    params['pz'] = 200
    params['pn'] = 1
    params['fltt'] = 2
    params['invt'] = 2
    params['ut'] = 'b2884a393a59ad64002292a3e90d46a5'
    params['fs'] = 'm:90 t:2'
    params['fields'] = 'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124'
    df = requests.get(url, params=params)
    jsonp = loads_jsonp(df.text)
    if jsonp:
        data = jsonp.get('data')
        print(data)
        diff = data.get('diff')
        total = data.get('total')
        print(f'total={total}')
        all_industry = []
        for i in range(total):
            item = diff.get(str(i))
            dest_info = transfer_fields(item)
            dest_info['source'] = '东方财富'
            all_industry.append(dest_info)
            data_uploader_helper.upload_one(dest_info, 'industry_money_flow')
        return all_industry


def job_function():
    if data_uploader_helper.is_trade_day():
        all_industry = get_industry()
        if all_industry:
            dumps = json.dumps(all_industry, indent=4, ensure_ascii=False)
            print(dumps)


if __name__ == '__main__':
    job_function()
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('45 18 * * *'))
    sched.start()
