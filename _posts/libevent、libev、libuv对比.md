---
title: libevent、libev、libuv对比
date: 2019-03-02 10:44:17
tags:
	- 网络

---



```
简单说，是这样的关系：
1、libevent，最早出现。使用广泛。
2、libev。去掉了libevent里对windows的支持，代码更加简洁了。
3、libuv。更换了底层机制，也兼容了windows。

libuv，是目前实用的。libev用得不多。
```



libevent :名气最大，应用最广泛，历史悠久的跨平台事件库；

libev :较libevent而言，设计更简练，性能更好，但对Windows支持不够好；

libuv :开发node的过程中需要一个跨平台的事件库，他们首选了libev，但又要支持Windows，故重新封装了一套，linux下用libev实现，Windows下用IOCP实现；



可见，目前libuv的影响力最大，其次是libevent，libev关注的人较少。



Libevent、libev、libuv三个网络库，

都是c语言实现的异步事件库*Asynchronousevent library）* 。

异步事件库本质上是**提供异步事件通知**（Asynchronous Event Notification，AEN）的。

异步事件通知机制就是**根据发生的事件，调用相应的回调函数进行处理。**



**事件（Event）：** 

事件是异步事件通知机制的核心，

比如fd事件、超时事件、信号事件、定时器事件。

有时候也称事件为事件处理器（EventHandler），这个名称更形象，因为Handler本身表示了包含处理所需数据（或数据的地址）和处理的方法（回调函数），更像是面向对象思想中的称谓。

**事件循环（EventLoop）：** 等待并分发事件。事件循环用于管理事件。



# libevent和libev详细对比

我当前对libev用得比较多了。

看到libev也提供了一个libevent的接口兼容层（但是我估计只是实现了基本功能，因为libev的功能比libevent少）。

| 特性      | libevent                                                     | libev   |
| --------- | ------------------------------------------------------------ | ------- |
| 优先级    | event的被放入在优先级队列里。event的优先级默认相同。可以设置高优先级得到优先处理。 | 一样    |
| eventloop | event_bsae                                                   | ev_loop |
| 线程安全  | event_base和loop都不是线程安全的。一个event_base只能在在一个线程里访问。 |         |



# 参考资料

1、简单对比 Libevent、libev、libuv

https://yq.aliyun.com/articles/611321

2、

https://juejin.cn/post/6963589981797351460