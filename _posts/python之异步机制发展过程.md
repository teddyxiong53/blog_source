---
title: python之异步机制发展过程
date: 2023-10-01 11:41:11
tags:
	- python
---

--

Python的异步编程机制在过去几年中经历了不断的发展和演变。下面是Python异步机制的主要发展过程：

1. **回调（Callback）**：在早期的Python版本中，使用回调函数是处理异步任务的主要方法。当一个异步任务完成时，会调用预先定义的回调函数来处理结果。这种方式需要手动管理回调函数的嵌套和执行顺序，容易导致代码复杂和难以维护。

2. **生成器（Generator）**：Python 2.5引入了生成器（Generator）作为一种半同步半异步的编程模型。通过使用`yield`语句，可以将函数转换为生成器函数，并使用生成器迭代器进行异步操作。生成器提供了一种简单的方式来处理异步任务，但仍需要手动管理生成器的状态和调度。

3. **协程（Coroutine）**：Python 3.4引入了`asyncio`模块，它基于协程（Coroutine）的异步编程模型。协程是一种特殊的生成器函数，可以通过`async`和`await`关键字进行定义和调用。使用协程，可以编写类似于同步代码的异步程序，而无需手动管理生成器的状态和调度。`asyncio`提供了事件循环（Event Loop）和异步IO操作的支持，使得异步编程更加方便和高效。

4. **async/await语法**：Python 3.5引入了`async`和`await`关键字，用于定义和调用协程。`async`用于定义协程函数，`await`用于等待协程的执行结果。这种语法使得异步代码更加清晰和易读，减少了对生成器的直接操作。

5. **异步上下文管理器和异步迭代器**：Python 3.7引入了异步上下文管理器（Async Context Manager）和异步迭代器（Async Iterator）的概念。它们与普通的上下文管理器和迭代器类似，但是支持异步操作。异步上下文管理器可以通过`async with`语法进行使用，而异步迭代器可以通过`async for`语法进行遍历。这些概念进一步扩展了异步编程的能力和灵活性。

这些发展过程使得Python的异步编程变得更加强大和易用，使开发者能够更好地处理IO密集型任务和并发操作。异步编程在Web开发、网络通信、并发任务等领域得到广泛应用。

# 回调方式

这个不看了。

# 生成器方式

```
import time

def async_operation():
    # 模拟异步操作，比如网络请求或IO操作
    time.sleep(2)
    yield "异步操作完成"

def main():
    print("开始异步操作")
    gen = async_operation()
    result = next(gen)
    print("异步操作结果:", result)

# 执行主程序
main()
print("异步操作进行中...")
```

这个例子并不合适。

# asyncio方式

```
import asyncio

async def async_operation():
    # 模拟异步操作，比如网络请求或IO操作
    await asyncio.sleep(2)
    return "异步操作完成"

async def main():
    print("开始异步操作")
    result = await async_operation()
    print("异步操作结果:", result)

# 创建事件循环并运行异步任务
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

