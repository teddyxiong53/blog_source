---
title: Python之apscheduler
date: 2017-11-20 11:55:05
tags:
	- Python
	- 调度

---



我在看叮当这个开源音箱的代码的时候，看到了apscheduler这个东西，现在学习一下。

# 1.什么是apscheduler

在编程中，定时任务调度是一种常见的调度方式。Python中常用的就是apscheduler。

apscheduler是基于Quartz的Python定时任务框架。实现了Quartz的所有功能。提供了基于日期、固定时间间隔以及crontab类型的任务。并且可以持久化任务。

可以很方便地与redis、数据库等第三方进行协同工作。

特点就是简单而且强大。

在Python世界里，另外还有一个与apscheduler齐名的调度模块Celery。Celery是分布式的调度器。

# 2. 重要概念

在apscheduler里，有几个非常重要的概念，需要先进行了解。

1、触发器。trigger。

包含调度逻辑，每个job有他自己的触发器。触发器定义了时间点、频率等参数。

2、作业存储。job store。

默认是存在内存里。你可以设置保存到数据库里。

3、执行器。executor。

4、调度器。scheduler。

一个App里，一般只有一个调度器。

常用的调度器有这些：

```
1、BlockingScheduler。跟直接调度函数没有什么区别，会阻塞当前进程。
2、BackgroundScheduler。这个常用，有点像创建一个线程去执行一个耗时的操作。
其他的就先不看了。
```

实际上，一般就是用BackgroundScheduler。

# 3.先看一个简单例子

```
#!/usr/bin/python 

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval',seconds=3)
def timed_job():
    print "this job works every 3 seconds"
    
@sched.scheduled_job('cron', day_of_week="mon-fri", hour="0-9", minute="30-59",second="*/3")
def scheduled_job():
    print "this job works every weekday"
    
print "before start scheduler"
sched.start()
print "after scheduler"

```

这个例子里，是用装饰器来添加的任务，这种方式不是很符合我的习惯，当然还是有对应的函数来做的。

# 4.常用函数接口









