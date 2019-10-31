---
title: 异步Python之aiohttp
date: 2019-10-18 15:35:49
tags:
	- Python

---

1

aiohttp是跟requests类似的东西，只是requests是同步的，而aiohttp是异步的。

基本的使用代码是这样：

```
import asyncio
from aiohttp import ClientSession

tasks = []
url = 'https://www.baidu.com/{}'
async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(hello(url))
```

同时访问多个url，该怎么做呢？

```
import asyncio
from aiohttp import ClientSession
import time

tasks = []
url = 'https://www.baidu.com/{}'
async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            # print(response)
            print('hello time:{}'.format(time.time()))

def run():
    for i in range(5):
        task = asyncio.ensure_future(hello(url.format(i)))
        tasks.append(task)

loop = asyncio.get_event_loop()
run()
loop.run_until_complete(asyncio.wait(tasks))

```

上面我们只是发出了请求，但是没有收集返回的结果。

这里就可以借助于asyncio.gather函数来做。

```
import asyncio
from aiohttp import ClientSession
import time

tasks = []
url = 'https://www.baidu.com/{}'
async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            # print(response)
            print('hello time:{}'.format(time.time()))
            return  await response.read()

def run(loop):
    for i in range(5):
        task = asyncio.ensure_future(hello(url.format(i)))
        tasks.append(task)
    result = loop.run_until_complete(asyncio.gather(*tasks))
    print(result)

loop = asyncio.get_event_loop()
run(loop)
```

异常处理

如果你的并发达到2000个，而且如果你使用的是select来做事件循环的底层机制，就会报错。

我们有三种方法解决这个问题：

```
1、限制并发数量。
2、使用回调的方式 。
3、修改os的文件限制。
```

限制并发数量是比较好的方式。

```
import asyncio
from aiohttp import ClientSession
import time

tasks = []
url = 'https://www.baidu.com/{}'

async def hello(url, semaphore):
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

async def run():
    semaphore = asyncio.Semaphore(500)
    to_get = [hello(url.format(i), semaphore) for i in range(1000)]
    await asyncio.wait(to_get)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.close()
```





参考资料

1、python异步编程之asyncio（百万并发）

https://www.cnblogs.com/shenh/p/9090586.html