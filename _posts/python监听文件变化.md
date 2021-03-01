---
title: python监听文件变化
date: 2021-02-24 09:50:30
tags:
- python
---

--

现在需要在修改配置文件的时候，自动重新解析参数。

需要就需要监听配置文件的变化。

python里如何做呢？

在python中文件监控主要有两个库，

一个是pyinotify （ https://github.com/seb-m/pyinotify/wiki ），

一个是watchdog（http://pythonhosted.org/watchdog/）。

pyinotify依赖于Linux平台的inotify，

后者则对不同平台的的事件都进行了封装。

因为我主要用于Windows平台，所以下面着重介绍watchdog（推荐大家阅读一下watchdog实现源码，有利于深刻的理解其中的原理）。 



参考资料

1、

https://cloud.tencent.com/developer/article/1567515