---
title: Python之asyncio（3）
date: 2019-11-14 17:37:48
tags:
	- Python

---

--

目前对asyncio还没有真正理解。

所以通过例子来加深认识。

写一个tcp client，基于asyncio。

准备服务器：

```
python3 -m http.server
```

这样就启动了一个简单的http服务器。很方便。

写client代码，如下：

```
import asyncio
HOST='192.168.56.101'

class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        request = 'GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(HOST)
        transport.write(request.encode())

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exc):
        self.loop.stop()

async def main(loop):
    await loop.create_connection(
        lambda : ClientProtocol(loop), HOST, 8000
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop)) #其实运行2两次。不太合适，后面要改。
loop.run_forever() # 
```

上面这个代码，在connection_made里，手动构建了http请求，无疑是非常不灵活的。

我们新建一个ClientSession类。

```

```

# Awaitable对象

如果一个对象可以在 [`await`](https://docs.python.org/zh-cn/3/reference/expressions.html#await) 语句中使用，那么它就是 **可等待** 对象。许多 asyncio API 都被设计为接受可等待对象。

*可等待* 对象有三种主要类型: **协程**, **任务** 和 **Future**.

什么是协程？

就是async def的函数。

# asyncio.Protocol

`asyncio.Protocol` 是 asyncio 中的一个基类，用于实现网络协议。它提供了一种编写基于流的协议的方式，例如 TCP、UDP 或 SSL。

`asyncio.Protocol` 定义了一组方法，子类可以重写这些方法来实现自定义的协议逻辑。以下是一些常用的方法：

1. `connection_made(transport)`：当与远程主机建立连接时调用。可以在该方法中执行一些初始化操作，如设置连接状态、发送初始数据等。

2. `data_received(data)`：当接收到数据时调用。传入的参数 `data` 是接收到的字节流。在该方法中可以处理接收到的数据，解析协议等。

3. `connection_lost(exc)`：当连接丢失或关闭时调用。传入的参数 `exc` 表示连接关闭的原因，可以是异常对象或 `None`。在该方法中可以执行一些清理操作。

4. `eof_received()`：当接收到 EOF（End of File）时调用。EOF 表示数据流的结束。该方法用于处理数据流的结束信号。

通过继承 `asyncio.Protocol` 类并实现上述方法，可以创建自定义的协议处理类。然后可以将该协议处理类与事件循环结合使用，通过调用 `loop.create_server()` 或 `loop.create_connection()` 来建立网络连接，并处理传入和传出的数据。

示例代码如下：

```python
import asyncio

class MyProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        # 连接建立时调用
        print("Connection made.")

    def data_received(self, data):
        # 接收到数据时调用
        print("Received data:", data.decode())

    def connection_lost(self, exc):
        # 连接关闭时调用
        print("Connection lost.")

loop = asyncio.get_event_loop()
coro = loop.create_server(MyProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
```

上述示例中，`MyProtocol` 继承自 `asyncio.Protocol`，实现了 `connection_made()`、`data_received()` 和 `connection_lost()` 方法来处理连接、接收数据和连接关闭的逻辑。通过调用 `loop.create_server()` 创建服务器，并将 `MyProtocol` 作为协议处理类传入。然后通过调用 `loop.run_forever()` 运行事件循环，处理传入的连接和数据。

使用 `asyncio.Protocol` 可以方便地实现自定义的网络协议处理逻辑，适用于构建各种基于流的网络应用。

# 代码目录分析

以下是 asyncio 源代码中一些核心文件的作用简介：

1. `asyncio/__init__.py`：asyncio 库的入口文件，定义了导入 asyncio 时可用的公共接口，包括创建事件循环、运行事件循环等。

2. `asyncio/base_events.py`：定义了事件循环的基础类 `BaseEventLoop`，以及其他与事件循环相关的类和函数。包括事件循环的创建、启动和停止，以及处理任务调度、回调处理等。

3. `asyncio/events.py`：定义了事件和回调相关的类和函数，包括 `Event`、`Future`、`Task` 等。它们用于在异步编程中管理和处理事件、回调和异步操作的状态和结果。

4. `asyncio/tasks.py`：定义了任务相关的类和函数，包括 `ensure_future`、`wait`、`gather` 等。它们用于创建和管理协程任务，并提供了协程的调度和并发执行的功能。

5. `asyncio/protocols.py`：定义了协议相关的基类和接口，包括 `Protocol`、`Transport` 等。它们用于实现网络协议和流程控制，并提供了与传输和网络通信相关的抽象。

6. `asyncio/futures.py`：定义了与 Future 相关的类和函数，用于表示异步操作的结果。包括 `Future`、`CancelledError` 等，用于处理异步操作的完成和取消状态。

7. `asyncio/selector_events.py`：实现了基于选择器的事件循环，用于处理底层的 I/O 操作。它使用系统提供的选择器来监听文件描述符的事件，并将其集成到 asyncio 的事件循环中。



# `__await__ = __iter__` 

`__await__ = __iter__` 是在实现可迭代对象时的一种常见模式，

用于定义可迭代对象的迭代行为和异步迭代行为。

在 Python 中，可迭代对象是指实现了 `__iter__()` 方法的对象，

该方法返回一个迭代器对象，

用于支持迭代操作。

迭代器对象可以通过 `next()` 方法逐个返回元素，

直到抛出 `StopIteration` 异常表示迭代结束。



在异步编程中，可以使用 `await` 关键字来暂停异步函数的执行，等待一个异步操作完成。

为了支持异步迭代操作，

Python 提供了 `__aiter__()` 和 `__anext__()` 方法，

它们分别对应于普通迭代器的 `__iter__()` 和 `next()` 方法。



为了简化代码，

避免在实现异步迭代器时重复编写相似的方法，

可以使用 `__await__ = __iter__` 的方式。

**这样做的效果是将 `__iter__()` 方法也作为异步迭代器的方法，**

**使得对象可以同时支持普通迭代和异步迭代。**



以下是一个示例，展示了如何使用 `__await__ = __iter__` 实现同时支持普通迭代和异步迭代的对象：

```python
class MyAsyncIterable:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return iter(self.data)

    __await__ = __iter__

async def main():
    async for item in MyAsyncIterable([1, 2, 3]):
        print(item)

if __name__ == "__main__":
    asyncio.run(main())
```

在上述示例中，我们定义了一个 `MyAsyncIterable` 类，

它实现了 `__iter__()` 方法和 `__await__()` 方法。

由于 `__await__ = __iter__`，

**对象可以同时被普通 `for` 循环和异步 `async for` 循环使用。**

在 `main()` 异步函数中，我们使用异步迭代来遍历 `MyAsyncIterable` 对象，并打印每个元素。

通过使用 `__await__ = __iter__`，我们可以方便地在一个对象中实现同时支持普通迭代和异步迭代的行为，提高代码的可复用性和一致性。

# 实现echo server

```
import asyncio

async def handle_client(reader, writer):
    while True:
        data = await reader.readline()
        if not data:
            break
        writer.write(data)
        await writer.drain()

    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())

```

# `__aenter__`用法

```
import asyncio
class AsyncContextManager:
    async def __aenter__(self):
        # 执行初始化操作并返回一个对象
        print("Entering context")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 执行清理操作
        print("Exiting context")

async def main():
    async with AsyncContextManager() as cm:
        # 在上下文管理器中执行操作
        print("Inside context")

asyncio.run(main())


```

# Future和Task关系

在 `asyncio` 中，`Future` 和 `Task` 都是用于管理异步操作的对象，它们之间存在一些关系和区别。

1. Future（未来对象）：
   - `Future` 是 `asyncio` 中的一个类，表示一个异步操作的结果或状态。
   - `Future` 对象通常用于封装异步操作的结果，并在异步操作完成时获取结果或处理异常。
   - `Future` 对象可以手动设置结果或异常，也可以由 `asyncio` 相关的方法或类自动设置。
   - `Future` 对象的状态可以是挂起、完成或取消。
   - `Future` 提供了一些方法和属性，如 `add_done_callback()`、`result()`、`exception()` 等，用于处理异步操作的结果和状态。

2. Task（任务对象）：
   - `Task` 是 `asyncio` 中的一个子类，表示一个可调度的协程对象（`coroutine`）。
   - `Task` 是对 `Future` 对象的进一步封装，它继承了 `Future` 的功能，并提供了额外的调度功能。
   - `Task` 对象通常由事件循环的 `create_task()` 方法创建，并将一个协程对象包装为 `Task`。
   - `Task` 对象可以被事件循环调度执行，可以暂停和恢复执行，并且可以取消执行。
   - `Task` 提供了一些方法和属性，如 `cancel()`、`done()`、`result()`、`exception()` 等，用于操作和查询任务的状态和结果。

关系：
- `Task` 是 `Future` 的子类，因此 `Task` 对象也是 `Future` 对象。
- 每个 `Task` 对象都是一个 `Future` 对象，它具有 `Future` 对象的所有功能和特性。
- `Task` 对象具有额外的调度功能，可以被事件循环调度执行。
- 通过 `create_task()` 方法将协程对象封装为 `Task` 对象，可以更方便地在事件循环中管理和调度协程。

总结而言，`Future` 和 `Task` 都用于管理异步操作，其中 `Future` 表示一个异步操作的结果或状态，而 `Task` 是对 `Future` 的进一步封装，表示一个可调度的协程对象。`Task` 对象是 `Future` 对象的子类，具有 `Future` 的功能，并提供了额外的调度功能。通过 `Task` 对象，可以方便地在事件循环中管理和调度协程。

# 参考资料

1、Python 的异步 IO：Asyncio 之 TCP Client

https://segmentfault.com/a/1190000012286062