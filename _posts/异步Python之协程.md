---
title: 异步Python之协程
date: 2019-10-31 13:21:49
tags:
	- Python

---

1

协程使用async和await语法来定义。

HelloWorld是这么写的：

```
import asyncio
async def main():
    print("hello ")
    await asyncio.sleep(1)
    print("world")

asyncio.run(main())
```

如果是直接调用协程，是不会执行的：

```
main() #这样并不会执行。
```

要真正运行一个协程，asyncio提供了三种主要的机制：

```
1、使用asyncio.run()
2、用await来调用一个协程。
3、用asyncio.create_task()
```

看看await调用的方式。

```
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(1)
    print(what)

async def main():
    print("start at {}".format(time.time()))
    await say_after(1, 'hello')
    await say_after(2, 'world')
    print("end at {}".format(time.time()))

asyncio.run(main())
```

看看create_task的方式。

```
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    print('start at {}'.format(time.time()))
    await task1
    await task2
    print('end at {}'.format(time.time()))


asyncio.run(main())
```



可等待对象

一个一个对象看一看放在await后面使用，那么它就是一个可等待对象。

许多asyncio API都被设计为接受可等待对象作为参数。

可等待对象有三种类型：

```
1、协程。
2、任务。
3、future。
```

上面举的例子已经看过协议和任务的了。

Future是一种特殊的低层级的可等待对象，表示一个异步操作的结果。

当一个future对象被等待，意味着协程将保持等待直到该future对象在其他地方操作完成。



sleep

```
import asyncio
import datetime

async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if(loop.time() + 1.0 >= end_time):
            break
        await asyncio.sleep(1)

asyncio.run(display_date())
```



并发执行任务

asyncio.gather

```
参数1：
	aws。表示可等待对象集。
参数2：
	loop。默认为None。
	在python3.8开始被设置为过时。在3.10里会被移除。
参数3：
	return_exceptions。默认为False。
	表示的含义是：出现异常的任务，会马上把异常传递给等待gather的函数。
	aws里的其他的任务不会受到影响。
```

如果gather被取消，aws里的任务都会被取消。

```
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print("task {}: compute factorial {}".format(name, i))
        await asyncio.sleep(1)
        f *= i
    print("task {}: factorial({})={}".format(name, number, f))
async def main():
    await asyncio.gather(factorial('A', 2), factorial('B', 3), factorial('C', 4))

asyncio.run(main())
```



屏蔽取消操作

asyncio.shield

```
参数1：
	aw。一个可等待对象。
参数2：
	loop。默认为None。这个参数后面还是会去掉。
```



超时

asyncio.wait_for

```
参数1：
	aw。
参数2：
	timeout。
```

```
import asyncio

async def eternity():
    await asyncio.sleep(3600)
    print('yay')

async def main():
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except asyncio.TimeoutError:
        print("timeout")

asyncio.run(main())
```



参考资料

1、协程与任务

https://docs.python.org/zh-cn/3/library/asyncio-task.html#coroutine