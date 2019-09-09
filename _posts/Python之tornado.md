---
title: Python之tornado
date: 2018-05-18 21:50:08
tags:
	- Python

---



tornado是一个Python写的web框架。字面意思是龙卷风。

它的特点是：

非阻塞，速度快。

它的原理是使用了非阻塞方式和epoll。

每秒可以处理数以千计的连接。

# 基本例子

```
#!/usr/bin/env python

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("hello tornado")
		
application = tornado.web.Application(
	[
		(r"/index", MainHandler),
	]
)

application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
```

访问这个地址：

http://192.168.0.9:8888/index

就可以得到页面了。

这个逻辑跟Flask和类似。



web framework的定义。

是指一组包或者模块，可以帮助开发者编写web app，让开发者不用关心底层的协议、socket处理或进程线程。



tornado作为web server，提供了web framework的api。可以直接用来构建自己的web app。



tornado跟其他的python web framework不同，它不是基于wsgi的。它是一个进程只有一个线程。

特点是异步编程。

tornado的代码不是线程安全的。

你可以通过`IOLoop.run_in_executor`来在另外一个线程里运行耗时的任务。

tornado6.0需要python3.5.2的支持。如果要兼容python2.7，使用tornado5.1版本。

tornado里的异步，是通过future机制来做的。

tornado推荐使用协程来做异步。

native协程还是装饰协程？

python3.5引入了async和await关键字。

如果你要兼容老版本的python，就使用装饰协程，如果不考虑兼容，就用native协程。

装饰协程

```
@gen.coroutine
def a():
    b =yield  c()
    raise gen.Return(b)
```

native协程

```
async def a():
    b = await c()
    return b
```

所有生成器都是异步的。当返回的时候，是返回一个生成器对象。

tornado.queues模块实现了一个异步生产者/消费者模型。



```
import time
from datetime import timedelta
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag

from tornado import gen, httpclient, ioloop, queues

base_url = 'http://www.tornadoweb.org/en/stable'
concurrency = 10

async def get_links_from_url(url):
    response = await httpclient.AsyncHTTPClient().fetch(url)
    print("fetch %s" % url)
    html = response.body.decode(errors="ignore")
    return [urljoin(url, remove_fragment(new_url)) for new_url in get_links(html)]

def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url

def get_links(html):
    class URLSeeker(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.urls = []

        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get("href")
            if href and tag == 'a':
                self.urls.append(href)

    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls

async def main():
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()

    async def fetch_url(current_url):
        if current_url in fetching:
            return
        print("fetching %s" % current_url)
        fetching.add(current_url)
        urls = await get_links_from_url(current_url)
        fetched.add(current_url)
        for new_url in urls:
            if new_url.startswith(base_url):
                await q.put(new_url)

    async def worker():
        async for url in q:
            if url is None:
                return
            try:
                await fetch_url(url)
            except Exception as e:
                print("exception: %s %s"  % (e, url))
            finally:
                q.task_done()

    await q.put(base_url)
    workers = gen.multi([worker() for _ in range(concurrency)])
    await q.join(timeout=timedelta(seconds=300))
    # assert fetching == fetched
    print("done in %d seconds, fetched %s urls" % (time.time() - start, len(fetched)))

    for _ in range(concurrency):
        await q.put(None)

    await workers

if __name__ == "__main__":
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)
```



# 参考资料

1、Tornado基本使用

https://www.cnblogs.com/chenchao1990/p/5413547.html

2、如何理解 Tornado ？

https://www.zhihu.com/question/20136991

3、

https://www.tornadoweb.org/en/stable/