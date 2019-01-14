---
title: 异步python之async和await入门
date: 2019-01-14 10:17:59
tags:
	- 异步
---



先从简单使用入手，把相关概念理清楚。

看下python里的函数的几种形式。

普通函数：

```
def function():
	return 1
```

生成器：

```
def generator():
	yield 1
```

异步函数（就是协程）：

```
async def async_function():
	return 1
```

异步生成器：

```
async def async_generator():
	yield 1
```



```
In [36]: async def do_work(): 
    ...:     pass 
    ...:                                             

In [37]: print(asyncio.iscoroutinefunction(do_work)) 
True
```



我们这样写：

```
import asyncio

async def do_some_work(x:int):
    print("waiting ...")
    await asyncio.sleep(x)

do_some_work(2)
print("end of code")
```

运行是不对的。

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ python3 ./test.py 
./test.py:7: RuntimeWarning: coroutine 'do_some_work' was never awaited
  do_some_work(2)
end of code
```

需要有一个loop才行。

调用协程函数，并不会运行，而是返回一个协程对象。

这样改：

```
import asyncio

async def do_some_work(x:int):
    print("waiting ...")
    await asyncio.sleep(x)
loop = asyncio.get_event_loop()
loop.run_until_complete(do_some_work(2))

print("end of code")
```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ python3 ./test.py 
waiting ...
end of code
```



回调

如果协程函数是进行io读写操作。我们希望在完成 后，得到通知，以便进行下一步的处理。

这个可以通过future来实现。

```
import asyncio

async def do_some_work(x:int):
    print("waiting ...")
    await asyncio.sleep(x)

def done_callback(fut):
    print("done")
loop = asyncio.get_event_loop()
fut = asyncio.ensure_future(do_some_work(3))
fut.add_done_callback(done_callback)
loop.run_until_complete(fut)
print("end of code")
```



多个协程

实际项目里，往往有多个协程。同时在一个loop里运行。

为了把多个协程交给一个loop，需要用asyncio.gather函数。

```
import asyncio
import time
async def do_some_work(x:int):
    print("waiting ...")
    await asyncio.sleep(x)


loop = asyncio.get_event_loop()
print("time before:%d" % time.time())
loop.run_until_complete(asyncio.gather(do_some_work(1), do_some_work(3)))
print("time after:%d" % time.time())
print("end of code")
```

可以看到，是以耗时比较长的那个为准了。

```
time before:1547445149
waiting ...
waiting ...
time after:1547445152
end of code
```

也可以放在list里。

```
coros = [do_some_work(1), do_some_work(3)]
loop.run_until_complete(asyncio.gather(*coros))
```



可以放多个future。

```
futs = [asyncio.ensure_future(do_some_work(1)), asyncio.ensure_future(do_some_work(3))]
loop.run_until_complete(asyncio.gather(*futs))
```



# 用asyncio写tcp的echo示例



参考资料

1、Python Async/Await入门指南

https://www.cnblogs.com/dhcn/p/9032461.html

2、用 Python 3 的 async / await 做异步编程

http://python.jobbole.com/88427/

3、Coroutines and Tasks

这个要3.7的才能跑起来。

https://docs.python.org/3/library/asyncio-task.html

这个3.6的可以。

https://docs.python.org/3.6/library/asyncio-task.html

4、Python 的异步 IO：Asyncio 简介

这篇教程很好。

https://segmentfault.com/a/1190000008814676

5、TCP echo client and server

https://asyncio.readthedocs.io/en/latest/tcp_echo.html

6、

https://docs.python.org/3/library/asyncio-eventloop.html