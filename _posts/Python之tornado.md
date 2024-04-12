---
title: Python之tornado
date: 2018-05-18 21:50:08
tags:
	- Python

---

--

tornado是一个Python写的web框架。字面意思是龙卷风。

它的特点是：

非阻塞，速度快。

它的原理是使用了非阻塞方式和epoll。

每秒可以处理数以千计的连接。

# 简介

Tornado是一个用Python编写的异步网络框架，最初由FriendFeed开发，并后来由Facebook维护。它专门设计用于构建高性能的、可伸缩的网络应用程序，特别适用于长连接的网络应用场景，如实时聊天、消息推送等。以下是Tornado的一些主要特点和优势：

1. **异步非阻塞IO模型：** Tornado采用了异步非阻塞的IO模型，使用单线程事件循环处理多个并发连接，提供了高效的IO操作。
  
2. **轻量级：** Tornado的核心非常精简，没有过多的依赖，使得它成为一个轻量级的网络框架。

3. **支持WebSocket：** Tornado原生支持WebSocket协议，使得开发实时Web应用变得更加简单。

4. **高性能：** 由于异步非阻塞的设计，Tornado在处理高并发请求时表现出色，适用于需要快速响应的应用场景。

5. **优秀的文档和社区支持：** Tornado拥有清晰的文档和活跃的社区，提供了丰富的示例代码和使用指南，便于开发者学习和使用。

6. **内置的HTTP服务器：** Tornado内置了一个高性能的HTTP服务器，使得开发者可以快速搭建起一个可用的Web应用环境，而无需额外的服务器软件。

7. **可扩展性：** Tornado提供了灵活的扩展接口，可以方便地集成其他Python库，实现更多功能的扩展。

总的来说，Tornado是一个功能强大、性能优异的异步网络框架，适用于构建高性能、实时的Web应用程序。



当前gpt能解析到的是6.10这个版本的，也算足够新的，就以这个为学习对象。

让chatgpt来教学。

# helloworld

以下是一个简单的 Tornado "Hello, World!" 示例代码：

```python
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, World!")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
```

在这个示例中：

- 首先，我们导入了 Tornado 所需的模块。
- 然后，我们定义了一个名为 `MainHandler` 的请求处理类，其中 `get` 方法用于处理 HTTP GET 请求，它向客户端发送 "Hello, World!"。
- 接着，我们定义了一个 `make_app` 函数，用于创建 Tornado 应用程序实例，并将 `MainHandler` 与 URL 路径 "/" 进行关联。
- 最后，在 `__main__` 部分，我们创建了应用实例，监听端口 8888，并启动了 Tornado I/O 循环。

运行该代码后，您可以在浏览器中访问 `http://localhost:8888`，应该会看到 "Hello, World!" 字样。

# tornado的主要api说明

Tornado 框架提供了许多重要的 API，用于构建异步 Web 应用程序。以下是一些主要的 Tornado API 及其简要说明：

1. **tornado.web.Application**:
   - 用于创建 Tornado 应用程序实例的类。
   - 参数通常是 URL 映射列表和其他设置项，例如调试模式、静态文件路径等。

2. **tornado.web.RequestHandler**:
   - 所有请求处理器类的基类，用于处理 HTTP 请求和生成 HTTP 响应。
   - 定义了一系列方法来处理不同类型的 HTTP 请求（如 GET、POST、PUT、DELETE）。

3. **tornado.web.HTTPRequest**:
   - HTTP 请求对象，包含了请求的各种信息，如请求方法、URL、请求头、请求体等。

4. **tornado.web.HTTPResponse**:
   - HTTP 响应对象，用于生成 HTTP 响应并发送给客户端。

5. **tornado.ioloop.IOLoop**:
   - Tornado 的核心事件循环类，用于管理事件的调度和执行。
   - 可以使用 `start()` 方法启动事件循环，监听并处理事件。

6. **tornado.gen**:
   - 包含了用于编写异步代码的工具，如 `coroutine` 装饰器和 `yield` 关键字。
   - 可以使用 `coroutine` 装饰器将普通函数转换为协程函数，以便在异步环境中使用。

7. **tornado.httpclient.HTTPClient** / **tornado.httpclient.AsyncHTTPClient**:
   - 用于发起 HTTP 请求的客户端类。
   - `HTTPClient` 提供同步的 HTTP 请求方法，而 `AsyncHTTPClient` 则提供了异步的 HTTP 请求方法。

8. **tornado.websocket.WebSocketHandler**:
   - 用于处理 WebSocket 连接的基类，可以接收和发送 WebSocket 消息。

9. **tornado.routing.Router**:
   - 用于定义 URL 路由规则的类，可以将 URL 映射到相应的请求处理器。

10. **tornado.template**:
    - Tornado 内置的模板引擎模块，用于渲染 HTML 模板文件。

11. **tornado.escape**:
    - 提供了一系列用于 HTML、JSON、URL 等编码和解码的函数，以及用于转义和过滤文本的工具函数。

这些是 Tornado 框架中一些常用的核心 API，通过它们可以实现各种类型的 Web 应用程序并处理各种类型的网络请求。

# tornado.ioloop.IOLoop.current().spawn_callback

`tornado.ioloop.IOLoop.current().spawn_callback` 方法用于在 Tornado 的当前事件循环中异步执行一个回调函数（即协程函数或普通函数）。这个方法在异步代码中非常有用，可以在不阻塞事件循环的情况下执行一些耗时的操作。

下面是这个方法的基本用法：

```python
import tornado.ioloop

async def my_async_function():
    # 异步操作
    await some_async_operation()

def my_callback():
    # 回调函数
    print("Callback executed")

# 在当前事件循环中异步执行回调函数
tornado.ioloop.IOLoop.current().spawn_callback(my_callback)
```

在这个示例中，`my_callback` 是一个普通的函数，通过 `spawn_callback` 方法将其添加到当前事件循环中执行。您也可以将异步函数（协程函数）传递给 `spawn_callback` 方法，Tornado 将会自动执行这个异步函数，并在执行完成后调用回调函数。

需要注意的是，使用 `spawn_callback` 方法执行的回调函数或异步函数不会阻塞当前的事件循环，因此可以在其内部执行一些耗时的操作而不会影响其他事件的处理。

# 基于tornado的项目目录结构说明

Tornado 框架的目录结构通常很简单，但是它可以根据项目的复杂程度和组织需求而有所变化。以下是一个基本的 Tornado 项目目录结构示例：

```
project/
│
├── handlers/          # 请求处理器目录
│   ├── __init__.py
│   └── main_handler.py    # 主要请求处理器
│
├── templates/         # 模板文件目录（可选）
│   └── index.html
│
├── static/            # 静态文件目录（可选）
│   ├── css/
│   ├── js/
│   └── img/
│
├── app.py             # 应用程序入口文件
│
└── requirements.txt   # 项目依赖的Python包列表
```

在这个目录结构中：

- `handlers/` 目录存放了请求处理器类文件。通常，每个请求处理器都会有一个单独的 Python 文件。在这个示例中，有一个名为 `main_handler.py` 的文件，里面包含了处理主要请求的请求处理器类。
  
- `templates/` 目录用于存放模板文件，如果你使用 Tornado 的模板引擎来生成动态内容的话。通常情况下，HTML 模板文件会放在这里。

- `static/` 目录存放静态文件，例如 CSS、JavaScript 和图像等。这些文件可以直接被客户端访问，而无需经过 Tornado 处理。

- `app.py` 是应用程序的入口文件，其中包含了 Tornado 应用程序的初始化代码和配置。

- `requirements.txt` 文件用于列出项目所依赖的 Python 包及其版本信息，方便在其他环境中重建项目所需的运行环境。

当然，根据项目的需要，目录结构可能会有所不同。例如，如果你的项目需要多个模块或子应用程序，可能会有更复杂的目录结构。

# 简介

Tornado 是一个 Python Web 框架和异步网络库，

最初由 FriendFeed 开发。

通过使用非阻塞网络 I/O，Tornado 可以扩展到数万个开放连接，

这使其成为长轮询、WebSocket 和其他需要与每个用户建立长期连接的应用程序的理想选择。



Tornado 与大多数 Python Web 框架不同。

它不基于 WSGI，

**并且通常每个进程仅使用一个线程运行。**

有关 Tornado 异步编程方法的更多信息，请参阅用户指南。

虽然tornado.wsgi模块中提供了对WSGI的一些支持，

但这不是开发的重点，

大多数应用程序应该编写为直接使用Tornado自己的接口（例如tornado.web），

而不是使用WSGI。



一般来说，Tornado 代码不是线程安全的。 

Tornado 中唯一可以从其他线程安全调用的方法是 IOLoop.add_callback。

您还可以使用 IOLoop.run_in_executor 在另一个线程上异步运行阻塞函数，

但请注意，传递给 run_in_executor 的函数应避免引用任何 Tornado 对象。 

run_in_executor 是与阻塞代码交互的推荐方式。



Tornado 与标准库 asyncio 模块集成，

并共享相同的事件循环（自 Tornado 5.0 起默认）。

一般来说，设计用于 asyncio 的库可以与 Tornado 自由混合。



大致可分为三个主要组成部分：

- 一个 Web 框架（包括 RequestHandler，它被子类化以创建 Web 应用程序，以及各种支持类）。
- HTTP 的客户端和服务器端实现（HTTPServer 和 AsyncHTTPClient）。
- 一个异步网络库，包括类 IOLoop 和 IOStream，它们充当 HTTP 组件的构建块，也可用于实现其他协议。

Tornado Web 框架和 HTTP 服务器一起提供了 WSGI 的全栈替代方案。

虽然可以使用 Tornado HTTP 服务器作为其他 WSGI 框架 (WSGIContainer) 的容器，

但这种组合有局限性，

要充分利用 Tornado，

**您需要同时使用 Tornado 的 Web 框架和 HTTP 服务器。**



实时 Web 功能需要每个用户有一个长期处于空闲状态的连接。

在传统的同步 Web 服务器中，这意味着为每个用户分配一个线程，这可能非常昂贵。

为了最大限度地降低并发连接的成本，

Tornado 使用单线程事件循环。

**这意味着所有应用程序代码都应该以异步和非阻塞为目标，**

**因为一次只能有一个操作处于活动状态。**

异步和非阻塞这两个术语密切相关，并且经常互换使用，但它们并不完全相同。



当函数在返回之前等待某些事情发生时，它就会阻塞。

一个函数可能会因多种原因而阻塞：

网络 I/O、磁盘 I/O、互斥体等。

事实上，每个函数在运行和使用 CPU 时至少会阻塞一点（举一个极端的例子，它演示了为什么 CPU 阻塞必须像其他类型的阻塞一样严肃对待，**请考虑像 bcrypt 这样的密码散列函数，它在设计上使用数百毫秒的 CPU 时间，远远超过典型的网络或磁盘访问**）。

函数可以在某些方面是阻塞的，而在其他方面可以是非阻塞的。

在 Tornado 的上下文中，我们通常在网络 I/O 的上下文中讨论阻塞，尽管各种阻塞都将被最小化。



异步函数在完成之前返回，并且通常会导致在触发应用程序中的某些未来操作之前在后台发生一些工作（与正常的同步函数相反，后者在返回之前完成它们要做的所有事情）。

异步接口有多种风格：

- 回调参数
- 返回占位符（Future、Promise、Deferred）
- 传送到队列
- 回调注册表（例如 POSIX 信号）

无论使用哪种类型的接口，

根据定义，异步函数与其调用者的交互方式都不同。

没有免费的方法可以以对其调用者透明的方式使同步函数异步

（像 gevent 这样的系统使用轻量级线程来提供与异步系统相当的性能，但它们实际上并不使事情异步）。

Tornado 中的异步操作通常返回占位符对象（Futures），

但一些低级组件（例如使用回调的 IOLoop）除外。

Future通常通过await 或yield 关键字转换为结果。



同步函数举例：

```
from tornado.httpclient import HTTPClient

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body
```

实现相同功能的异步实现：

```
from tornado.httpclient import AsyncHTTPClient

async def asynchronous_fetch(url):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url)
    return response.body
```

使用协程可以做的任何事情都可以通过传递回调对象来完成，

但是协程提供了重要的简化，

让您可以按照与同步时相同的方式组织代码。

这对于错误处理尤其重要，

因为 try/ except 块按照您在协程中的预期工作，而这很难通过回调实现。

本指南的下一部分将深入讨论协程。



协程是在 Tornado 中编写异步代码的推荐方法。

协程使用 Python wait 关键字来挂起和恢复执行，

而不是回调链（gevent 等框架中的协作轻量级线程有时也称为协程，但在 Tornado 中，所有协程都使用显式上下文切换并称为异步函数） 。

**协程几乎与同步代码一样简单，**

**但无需消耗线程。**

它们还通过减少可能发生上下文切换的位置数量，使并发性更容易推理。



Python 3.5 引入了 async 和await 关键字（使用这些关键字的函数也称为“原生协程”）。

为了与旧版本的Python兼容，您可以使用tornado.gen.coroutine装饰器来使用“装饰”或“基于产量”的协程。

只要有可能，本机协程是推荐的形式。

仅当需要与旧版本的 Python 兼容时才使用修饰协程。 Tornado 文档中的示例通常会使用本机形式。



Tornado 的tornado.queues 模块（以及 asyncio 中非常相似的 Queue 类）为协程实现了异步生产者/消费者模式，

类似于 Python 标准库的队列模块为线程实现的模式。

产生 Queue.get 的协程会暂停，

直到队列中有一个项目。

如果队列设置了最大大小，则生成 Queue.put 的协程将暂停，直到有空间容纳另一个项目。

队列维护未完成任务的计数，从零开始。 put 增加计数； task_done 会减少它。



在此处的网络蜘蛛示例中，队列开始时仅包含 base_url。

当worker获取页面时，它会解析链接并将新链接放入队列中，

然后调用 task_done 将计数器递减一次。

最终，worker 获取了一个其 URL 之前都已经见过的页面，并且队列中也没有剩余的工作。

因此，该worker对 task_done 的调用会将计数器递减至零。正在等待加入的主协程已取消暂停并完成。



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