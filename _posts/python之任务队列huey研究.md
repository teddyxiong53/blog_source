---
title: python之任务队列huey研究
date: 2023-01-20 17:07:31
tags:
	- Python

---



代码在这里：

https://github.com/coleifer/huey

# 什么是huey

* 一个任务队列。
* 用python写的。
* 简单干净的api。
* 可以存储到redis、sqlite、文件系统、或者in-memory。

## 支持这些特性

* 多进程、多线程、基于greenlet的协程。
* 在指定的时间执行任务。
* 调度周期性的任务，像crontab一样。
* 任务失败后重试。
* 任务优先级。
* 任务结果存储。
* 任务超时。
* 任务lock。
* 任务pipeline和chain。

# HelloWorld

task和periodic_task 这2个装饰器，可以用来把普通function转成task。

看一个简单的例子：

```
# demo.py
from huey import SqliteHuey

huey = SqliteHuey(filename='/tmp/demo.db')

@huey.task()
def add(a, b):
    return a + b
```

然后另外开一个shell仓库，执行命令：

```
huey_consumer demo.huey
```

huey_consumer是安装huey时被安装到全局的一个工具。

demo.huey表示的demo.py里的huey这个变量。

另外开一个shell窗口，进入到python解释器环境。

执行：

```
>>> from demo import add
>>> r = add(1, 2)
>>> r()
3
```

在生成的数据库文件里，是这样的情况：

```
sqlite> .tables
kv        schedule  task    
sqlite> select * from kv;
huey|fb862570-ecd7-48bd-8ccc-79a970e50ad1|.
sqlite> .schema kv
CREATE TABLE kv (queue text not null, key text not null, value blob not null, primary key(queue, key));
sqlite> .schema schedule
CREATE TABLE schedule (id integer not null primary key, queue text not null, data blob not null, timestamp real not null);
CREATE INDEX schedule_queue_timestamp on schedule (queue, timestamp);
sqlite> .schema task
CREATE TABLE task (id integer not null primary key, queue text not null, data blob not null, priority real not null default 0.0);
CREATE INDEX task_priority_id on task (priority desc, id asc);
sqlite> 
```

在huey_consumer的窗口，有这些打印：

```
[2023-01-20 17:41:55,080] INFO:huey.consumer:MainThread:The following commands are available:
+ demo.add
[2023-01-20 17:42:32,840] INFO:huey:Worker-1:Executing demo.add: fb862570-ecd7-48bd-8ccc-79a970e50ad1
[2023-01-20 17:42:32,840] INFO:huey:Worker-1:demo.add: fb862570-ecd7-48bd-8ccc-79a970e50ad1 executed in 0.000s
```

可以加延时：

```
>>> r = add.schedule((3,4), delay=5)
>>> r(blocking=True)
7
```

# 周期性任务

```
# demo.py
from huey import SqliteHuey, crontab

huey = SqliteHuey(filename='/tmp/demo.db')

@huey.task()
def add(a, b):
    return a + b

@huey.periodic_task(crontab(minute='*/1'))
def every_minute():
    print("every minute")
```

重新启动huey_consumer，就可以看到周期性任务在工作了。

# retry失败的任务

```
@huey.task(retries=2, retry_delay=3)
def flaky_task():
    if random.randint(0,1)==0:
        raise Exception('failing!')
    return 'OK'
```

测试：

```
>>> r = flaky_task.schedule(delay=1)
>>> r()
```



# 参考资料

1、官方文档

https://huey.readthedocs.io/en/latest/

