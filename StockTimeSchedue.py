#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2020/8/12 10:26
'''
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import main


def job_function():
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} start_main")
    main.start_main()


if __name__ == '__main__':
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{strftime} TimeSchedue  start")
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab('10 19 * * *'))
    sched.start()
