from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


def database_synchro():
    print("哈哈哈")


# 每2小时触发
sched.add_job(database_synchro, 'interval', hours=2, start_date='2019-08-13 12:53:00')

sched.start()



# # 在2009年11月6日执行
# sched.add_job(database_synchro, 'date', run_date=datetime(2019, 8, 13, 15, 46, 0), args=['text'])

sched.start()
