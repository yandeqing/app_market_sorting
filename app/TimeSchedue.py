#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/8/12 10:26
'''
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from app import main


def job_function():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    main.start_main()


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('10 9 * * *'))
    sched.start()