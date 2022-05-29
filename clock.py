import collections
from collections import abc
collections.MutableMapping = abc.MutableMapping
collections.Iterable = abc.Iterable
collections.Mapping = abc.Mapping
from apscheduler.schedulers.blocking import BlockingScheduler
from mail import Finmail

sched = BlockingScheduler(timezone="Asia/Shanghai")

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=21, minute=25)
def schedule_job():
    print('This job is running every weekday at 21:25')
    finmail = Finmail('')
    finmail.crawl()
    finmail.sendmail()

sched.start()
