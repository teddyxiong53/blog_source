---
title: 异步python之asyncio接口分析
date: 2019-01-14 14:31:59
tags:
	- 异步
---



这个主要是参考官方文档进行梳理。

asyncio是一个库，可以用async和await来写并发代码。

asyncio的api分为两种

1、上层api。

```
协程
streams
同步原语
子进程
队列
异常
```

2、底层api。

```
event loop
future
传输和协议
policies
Platform support
```



gather和wait，一般用gather就好了。



参考资料

1、Asynchronous I/O

https://docs.python.org/3/library/asyncio.html

2、Python中的asyncio代码详解

https://www.jb51.net/article/162705.htm