---
title: python之任务队列huey研究
date: 2023-01-20 17:07:31
tags:
	- Python

---



代码在这里：

https://github.com/coleifer/huey

# python的任务队列是什么，作用是什么

Python 中的任务队列是一种数据结构，

用于在多个执行单元（通常是线程或进程）之间传递任务或数据。

它的主要作用是协调和管理异步任务的执行，以提高系统的并发性能和可维护性。

任务队列通常用于以下几种情况：

1. **异步任务处理**：在异步编程中，任务队列可以用于将耗时的任务放入队列中，由后台线程或进程异步执行，以避免阻塞主程序的执行。

2. **并发任务处理**：在多线程或多进程的应用程序中，任务队列可以用于将任务分发给不同的执行单元，并协调它们的执行顺序，以实现并发处理。

3. **解耦系统组件**：通过将系统中的不同组件之间的通信和协作抽象成任务队列的方式，可以实现系统组件之间的解耦，提高系统的灵活性和可扩展性。

4. **缓解压力**：任务队列可以用于平衡系统中不同组件之间的负载，防止某一组件被过多的请求压垮，从而提高系统的稳定性和可靠性。

总的来说，任务队列提供了一种灵活而有效的机制，用于管理和调度系统中的任务和数据流，使得系统能够更好地适应复杂的并发和异步编程场景。

# Python任务队列方案有哪些

Python 中有几种常见的任务队列方案，每种都适用于不同的场景和需求。以下是其中一些：

1. **Queue 模块**：
   Python 的标准库中有一个 `queue` 模块，提供了多种队列实现，包括 FIFO 队列、LIFO 队列等。这些队列可以用于在多个线程之间进行通信和协调。

2. **Celery**：
   Celery 是一个流行的分布式任务队列，用于异步任务处理。它支持任务调度、任务结果存储、任务状态监控等功能，并提供了与常见的消息中间件（如 RabbitMQ、Redis 等）的集成。

3. **RQ (Redis Queue)**：
   RQ 是一个轻量级的 Python 库，用于将任务放入 Redis 队列中执行。它简单易用，适合于简单的任务队列需求。

4. **asyncio.Queue**：
   对于异步编程，Python 标准库中的 `asyncio` 模块提供了 `asyncio.Queue` 类，用于在异步任务之间进行通信。它适用于基于 asyncio 的异步应用程序。

5. **Kafka 和 RabbitMQ**：
   Kafka 和 RabbitMQ 是两个流行的消息中间件，它们提供了高级的消息队列功能，适用于需要高吞吐量和可靠性的分布式系统。Python 中有相应的客户端库，可以与它们进行交互。

6. **ZeroMQ**：
   ZeroMQ 是一个高性能的消息传递库，支持多种消息传输模式，包括队列模式。它适用于构建分布式系统中的通信通道。

这些方案各有特点，选择取决于你的具体需求，如性能要求、分布式支持、易用性等。

# redis queue介绍

https://github.com/rq/rq

Redis Queue（简称 RQ）是一个简单、轻量级的 Python 库，用于将任务放入 Redis 队列中执行。它的设计目标是简单易用，适用于基本的任务队列需求。

RQ 的核心思想是利用 Redis 的数据结构（如列表、哈希表等）来实现任务队列。具体而言，RQ 将任务封装成 Python 函数，并将函数及其参数序列化后存储在 Redis 的列表中。工作者进程从这个列表中取出任务，执行任务，并将执行结果存储在另一个 Redis 列表中。

RQ 的主要特点包括：

1. **简单易用**：RQ 的 API 设计简洁明了，易于上手和使用。

2. **轻量级**：RQ 代码库小巧，依赖少，适合于小型项目和简单的任务队列需求。

3. **基于 Redis**：利用 Redis 的高性能和可靠性，实现了简单而高效的任务队列。

4. **任务持久化**：RQ 使用 Redis 来持久化任务队列，确保任务不会在系统重启或崩溃时丢失。

5. **与 Flask、Django 等框架集成**：RQ 提供了与常见 Web 框架（如 Flask、Django 等）的集成支持，便于在 Web 应用中使用任务队列。

虽然 RQ 简单易用，但它也有一些局限性。例如，它不支持任务优先级、任务超时等高级特性，也不适合于大规模、高并发的任务队列需求。对于这些情况，可以考虑使用更复杂的任务队列系统，如 Celery。

## 代码举例

以下是一个简单的示例，演示如何使用 RQ 在 Python 中创建任务队列并执行任务：

首先，确保你已经安装了 RQ 和 Redis：

```bash
pip install rq redis
```

然后，创建一个 `tasks.py` 文件，定义一个简单的任务函数：

```python
# tasks.py

import time

def my_task(name):
    print(f"Starting task for {name}")
    # 模拟任务执行
    time.sleep(3)
    print(f"Task for {name} completed")
```

接下来，创建一个脚本来将任务提交到队列中：

```python
# submit_task.py

from redis import Redis
from rq import Queue
from tasks import my_task

# 连接到 Redis
redis_conn = Redis()

# 创建一个任务队列
queue = Queue(connection=redis_conn)

# 将任务提交到队列中
job = queue.enqueue(my_task, "Alice")

print("Task submitted to the queue")
```

最后，创建一个工作者进程来处理队列中的任务：

```bash
rq worker
```

运行 `submit_task.py` 脚本，将任务提交到队列中：

```bash
python submit_task.py
```

工作者进程将会从队列中取出任务并执行，你将会在终端上看到任务的输出。

这是一个简单的示例，演示了如何使用 RQ 创建任务队列并执行任务。在实际应用中，你可以根据需要对任务函数进行扩展，并利用 RQ 提供的 API 进行更多的配置和管理。

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

