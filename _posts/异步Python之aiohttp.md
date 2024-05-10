---
title: 异步Python之aiohttp
date: 2019-10-18 15:35:49
tags:
	- Python

---

--

# 简介

`aiohttp` 是一个基于 asyncio 的异步 HTTP 客户端/服务器框架，

用于处理 HTTP 请求和响应。

它提供了异步的 HTTP 客户端和服务器，

支持异步请求和响应处理，以及高性能的并发处理能力。

`aiohttp` 被广泛应用于编写异步的 Web 服务、HTTP 客户端、WebSocket 服务等。

以下是 `aiohttp` 的一些主要特点和功能：

1. **异步 IO 支持**：`aiohttp` 基于 asyncio 模块实现，采用异步 IO 模型，可以充分利用 Python 的异步特性，实现高性能的并发处理。

2. **HTTP 客户端和服务器**：`aiohttp` 提供了异步的 HTTP 客户端和服务器功能。您可以使用 `aiohttp.ClientSession` 类来创建异步的 HTTP 客户端，发送异步请求并处理异步响应；同时，您也可以使用 `aiohttp.web` 模块来创建异步的 HTTP 服务器，处理异步的 HTTP 请求和响应。

3. **WebSocket 支持**：除了 HTTP 协议，`aiohttp` 还提供了对 WebSocket 协议的原生支持。您可以使用 `aiohttp.web` 模块创建异步的 WebSocket 服务器，处理异步的 WebSocket 连接和消息。

4. **路由和中间件**：`aiohttp` 支持基于路由的 URL 分发和中间件处理，可以轻松地定义路由规则和中间件函数，并将它们应用到异步的 HTTP 请求处理过程中。

5. **SSL/TLS 加密支持**：`aiohttp` 支持使用 SSL/TLS 加密协议进行安全通信，可以配置异步的 SSL/TLS 加密连接，并实现安全的 HTTPS 通信。

6. **并发处理能力**：由于采用异步 IO 模型，`aiohttp` 具有很好的并发处理能力，可以处理大量的并发连接和请求，适用于高性能的 Web 服务和应用程序。

`aiohttp` 是一个功能强大、灵活且易于使用的异步 HTTP 客户端/服务器框架，广泛应用于异步编程和高性能的 Web 开发领域。

# aiohttp发展历史

`aiohttp` 的发展历史可以追溯到 2014 年左右。以下是 `aiohttp` 的主要发展历程：

1. **2014 年初**：
   - 最早的 `aiohttp` 版本由 Andrew Svetlov 创建，并在 GitHub 上发布。最初的版本提供了基本的异步 HTTP 客户端和服务器功能，基于 Python 3.3 中引入的 `asyncio` 标准库实现。

2. **2014 年中期**：
   - 随着 Python 3.4 的发布，`aiohttp` 开始吸引更多的关注和贡献者。该项目在 GitHub 上的活跃度增加，社区开始形成，并逐渐增加了更多的功能和改进。

3. **2015 年**：
   - `aiohttp` 的稳定版本发布，标志着项目进入了稳定的生命周期。该版本提供了完整的异步 HTTP 客户端和服务器功能，支持异步请求处理、路由分发、中间件处理等特性。

4. **2016 年**：
   - 随着 Python 3.5 的发布，`async` 和 `await` 关键字正式成为 Python 的核心语法，进一步推动了 `aiohttp` 的发展和普及。更多的开发者开始使用 `aiohttp` 来编写异步的 Web 服务和客户端应用程序。

5. **2017 年至今**：
   - `aiohttp` 持续保持活跃的开发和更新，不断引入新的功能和改进。项目的社区不断壮大，贡献者提供了大量的代码贡献、bug 修复和文档更新，使得 `aiohttp` 成为 Python 异步编程领域的重要组成部分。

在过去几年里，`aiohttp` 作为一个成熟的异步 HTTP 客户端/服务器框架，得到了广泛的应用和认可。它在处理高并发和大规模网络通信时表现出色，成为许多 Python 开发者的首选工具之一。

# aiohttp主要是做客户端吧。做服务端跟tornado对比怎样？

虽然 `aiohttp` 最初是作为一个异步 HTTP 客户端/服务器框架设计的，但是它同时提供了强大的异步 HTTP 服务器功能，使得开发者可以使用 `aiohttp` 构建异步的 Web 服务。

下面是 `aiohttp` 服务器与 `Tornado` 的一些比较：

1. **性能**：
   - `aiohttp` 和 `Tornado` 都是异步 IO 框架，具有良好的并发处理能力。在大多数情况下，`aiohttp` 和 `Tornado` 的性能都是非常接近的，都能够处理大量并发连接和请求。

2. **编程模型**：
   - `aiohttp` 使用的是 Python 3.5+ 引入的 `async/await` 语法，采用 asyncio 作为底层事件循环。因此，使用 `aiohttp` 编写的异步代码更符合 Python 的异步编程风格，更易于理解和维护。
   - `Tornado` 使用的是自己实现的事件循环，采用回调函数的方式处理异步任务。相比之下，`Tornado` 的编程模型可能会更加底层，需要更多的回调函数和事件处理。

3. **功能丰富程度**：
   - `Tornado` 是一个功能丰富的异步 IO 框架，提供了许多额外的功能，如 WebSocket 支持、模板引擎、用户认证等。它可以作为一个完整的 Web 开发框架来使用。
   - `aiohttp` 更加专注于 HTTP 客户端/服务器功能，提供了异步 HTTP 请求处理、路由分发、中间件处理等核心功能。虽然 `aiohttp` 也提供了 WebSocket 支持，但相比之下，`Tornado` 在 WebSocket 的支持上更加全面和成熟。

4. **社区和生态系统**：
   - `Tornado` 是一个成熟的框架，拥有庞大的用户社区和丰富的生态系统。您可以在社区中找到大量的插件、扩展和第三方库，以满足各种不同的需求。
   - `aiohttp` 作为一个比较新的框架，其社区和生态系统相对较小。但随着时间的推移，`aiohttp` 的用户社区和生态系统也在不断壮大，可以期待它的发展。

综上所述，`aiohttp` 和 `Tornado` 在异步 Web 开发领域都有各自的优势和适用场景。选择哪个框架取决于您的具体需求、编程偏好和项目特点。





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

# 异常处理

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



# 做服务端

所有的aiohttp服务器都围绕aiohttp.web.Application实例来构建。用于注册startup/cleanup信号，以及连接路由等。

参考资料

1、python异步编程之asyncio（百万并发）

https://www.cnblogs.com/shenh/p/9090586.html

2、

https://blog.csdn.net/u014028063/article/details/88016405