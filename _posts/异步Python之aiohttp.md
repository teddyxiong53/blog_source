---
title: 异步Python之aiohttp
date: 2019-10-18 15:35:49
tags:
	- Python

---

1

aiohttp是跟requests类似的东西，只是requests是同步的，而aiohttp是异步的。

简单使用

```
import asyncio, aiohttp

async def fetch_async(url):
    print(url)
    async with aiohttp.request('GET', url) as r:
        response = await r.text(encoding='utf-8')
        print("{} finished".format(url))
tasks = [
    fetch_async('http://www.baidu.com'),
    fetch_async('http://www.sina.com')
]
loop = asyncio.get_event_loop()
results = loop.run_until_complete(asyncio.gather(*tasks))
loop.close()
```

配合session，只需要修改上面的fetch_async函数即可。

```
async def fetch_async(url):
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status)
            await resp.text()
            print("{} finish".format(url))
```



参考资料

1、python---aiohttp的使用

https://www.cnblogs.com/ssyfj/p/9222342.html

