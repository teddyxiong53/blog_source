---
title: nodejs之事件循环
date: 2018-12-21 09:30:17
tags:
	- nodejs
---







在没有看资料之前，我先说一下我的基本想法。

我觉得nodejs跟单片机的前后台的机制有点像。

我们写的代码，依赖引擎给出类似中断的通知。



EventLoop允许nodejs执行非阻塞的io操作。尽管nodejs是单线程的。

因为现在的os都是多线程的。所以可以依赖os来通知操作的完成。

nodejs启动时，它就初始化了EventLoop，处理输入的脚本文件。



参考资料

1、Node.js 事件循环

http://www.runoob.com/nodejs/nodejs-event-loop.html