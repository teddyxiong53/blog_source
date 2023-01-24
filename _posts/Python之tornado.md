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



# 重新系统学习

就参考这个来学习。官网英文文档

https://www.tornadoweb.org/en/stable/

基于6.2版本。

## HelloWorld

先看HelloWorld

```
import tornado.ioloop
import tornado.web
import asyncio

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello world')

def make_app():
    return tornado.web.Application(
        [
            (r'/', MainHandler),
        ]
    )
async def main():
    app = make_app()
    app.listen(1408)
    await asyncio.Event().wait()

asyncio.run(main())
```

tornado跟flask等常见的python web框架不一样。

它不是基于wsgi的。

通常每个进程只运行一个线程。

当然，也提供了tornado.wsgi模块，但是一般不用。

写App的时候，应该使用tornado.web的接口。

而不是使用wsgi的接口。



通常情况下，tornado的代码不是线程安全的。

tornado里唯一可以安全地从其他线程里调用的函数是IOLoop.add_callback函数。

## 跟Python的asyncio整合

从5.0版本开始，tornado就跟python共用相同的eventloop。

tornado6.0需要Python3.7及以上的版本支持。



realtime的web App，需要每个user保持一个长连接，这个连接的绝大部分时间是idle状态的。

在一个传统的sync模式的web server，一般是给每个user分配一个thread，这个消耗太大了。

为了减小每个user的连接的cost，tornado使用了单线程加协程的方式。

这个意味着所有的代码都是异步和非阻塞的。

看看什么是同步的代码：

```
from tornado.httpclient import HTTPClient
def sync_fetch(url):
    http_client = HTTPClient()
    resp = http_client.fetch(url)
    return resp.body
```

异步的代码：

```
from tornado.httpclient import AsyncHTTPClient
async def sync_fetch(url):
    http_client = AsyncHTTPClient()
    resp = await http_client.fetch(url)
    return resp.body
```

# 代码层次

从tornado的源代码，梳理出所有的模块和class的类型层次关系。

代码量并不大。

所有的模块都是从`tornado/__init__.py`里进行导出的。

```
auth
	这个模块实现了第三方的授权模块。
	都是一些Mixin类，用来跟tornado.web.RequestHandler结合使用的。
	有两种使用方式：
	1、在login handler里，使用authenticate_redirect、authorize_redirect这些方法。
	2、再非login handler里，使用facebook_request、twitter_request这样的使用token去make request。
	有6个class。
	OpenIDMixin
	OAuthMixin
		TwitterMixin
	OAuth2Mixin
		GoogleOAuth2Mixin
		FacebookOAuth2Mixin
		
autoreload
	这个是用在debug的时候，在文件修改的时候，自动reload。
	使用是这样：
	python -m tornado.autoreload path/to/script.py [args...]
	代码不看了 。
	
concurrent
	提供Future这个class。
	之前是自己定义的，现在是使用asyncio.Future。
	提供一些工具函数，提供对之前方式的兼容。
	在代码上的体现是这样：
	Future = asyncio.Future
	FUTURES = (futures.Future, Future)
	函数里都带有future的字样。
	大部分都是future开头的。
	
curl_httpclient
	既有pycurl实现的非阻塞的http client。
	主要就是这个类。有500行。
	class CurlAsyncHTTPClient(AsyncHTTPClient):
escape
	对文本进行处理。
gen
	实现基于generator的协程。
	对于现在不需要了。老代码才需要。
	
http1connection
	http/1.X的 server和client实现。
	最复杂的是这个类。
	class HTTP1Connection(httputil.HTTPConnection)
	有600行。
httpclient
	提供阻塞和非阻塞2种http client。
	实现了二者共用的一些接口。
	simple_httpclient
	curl_httpclient
	默认使用的是simple_httpclient的方案。
	有这些需求，可以切换为使用curl_httpclient。
	1、复杂的。
	2、更快的。
	class HTTPClient
	class AsyncHTTPClient(Configurable)
	class HTTPRequest(object)
	class HTTPResponse(object)
	class HTTPClientError(Exception)
httpserver
	对外主要是这个类：
	class HTTPServer(TCPServer, Configurable, httputil.HTTPServerConnectionDelegate)
httputil
	被server和client共用的一些代码。
	代码比较多，有1200行。
	
ioloop
	从6.0开始，IOLoop是对asyncio的eventloop的包装。
	提供对之前方案的兼容。
	class IOLoop(Configurable)
	这个类有700行。
	
iostream
	提供工具类用来非阻塞读写socket。
	class BaseIOStream(object)
	这个类有800行。
	
locale
	进行本地化。
	这样使用：
	user_locale = tornado.locale.get("es_LA")
    print(user_locale.translate("Sign out"))
locks
	提供一些同步机制。
log
	提供一下log函数，还是基于logging的。
	
netutil
	提供一些网络工具函数。
options
	对参数进行解析的。
platform
	这个是一个目录。
	有几种选择，有asyncio和twisted。就看asyncio的就好了。
	asyncio的不用了。
process
	多进程管理。
queues
	一些队列相关的类。不知道为什么要这个。都是非线程安全的。
routing
	路由相关。
simple_httpclient
	
tcpclient
tcpserver
template
testing
util
web
	这个文件很重要。
	对外提供Application
	RequestHandler 这个有1600行。
```

# 官方example

就在代码的demos目录下。

## HelloWorld

```
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
```

define 这个函数定义了一个选项。

使用上看起来比较直观。

```
http_server.listen(options.port)
```

## TCP echo

官方的是用了gen的，只要去掉gen改成async的，然后yield的地方，改成await，也是可以的。



# 参考资料

1、Tornado基本使用

https://www.cnblogs.com/chenchao1990/p/5413547.html

2、如何理解 Tornado ？

https://www.zhihu.com/question/20136991

3、

https://www.tornadoweb.org/en/stable/