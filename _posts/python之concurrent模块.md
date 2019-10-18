---
title: python之concurrent模块
date: 2019-10-18 15:49:49
tags:
	- Python

---

1

python标准库为我们提供了threading和multiprocessing这2个模块，帮忙我们进行多线程和多进程编程。

从python3.2开始，标准库提供了concurrent模块。

这个模块里的futures模块。提供了ThreadPoolExecutor和ProcessPoolExecutor。来进行并发编程。

而asyncio重点是用用协程来实现并发。所以更加有前途。

```
import time
from concurrent.futures import ThreadPoolExecutor

def task(msg):
    time.sleep(1)
    return msg

pool = ThreadPoolExecutor(max_workers=3)
task1 = pool.submit(task, '11')
task2 = pool.submit(task, '22')
print("is task1 done? ", task1.done())
time.sleep(4)
print(task1.result())
print(task2.result())

```





参考资料

1、简单实现并发：python concurrent模块

https://www.cnblogs.com/kylinfish/articles/4352709.html

2、Python并发concurrent.futures和asyncio

https://blog.csdn.net/qq_29287973/article/details/78518595