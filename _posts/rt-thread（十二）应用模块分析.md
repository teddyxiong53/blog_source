---
title: rt-thread（十二）应用模块分析
date: 2018-02-05 23:07:37
tags:
	- rt-thread

---



rt-thread支持应用模块。打开方法是配置RT_USING_MODULE。

应用模块机制，可以让rt-thread的os跟应用不编译成一个整体。应用可以单独编译，放在SD卡上，然后os启动上，再执行应用。

但是这个有个限制，就是必须在ram里运行。不过对我来说，没有问题。我都是在ram里用的 。

最新的版本，已经从example目录下去掉了module的例子。不知道为什么。

我们可以从老的版本里拷贝一个例子出来，编译运行看看。





