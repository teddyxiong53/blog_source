---
title: Android系统之MessageQueue
date: 2020-09-14 15:00:32
tags:
	- Android系统

---

1

Android 中有两个非常重要的知识点，分别是Binder机制和Handler机制。

前者用于**跨进程通讯**，并且通过 ServiceManager 给上层应用提供了大量的服务，

而后者用于**进程内部通讯**，以消息队列的形式驱动应用的运行。

之前的文章已经多次分析了Binder相关的内容，复杂程度远高于Handler，之后还会继续分析Binder。

说到Handler，做安卓开发的一定都不会陌生，一般用于切换线程。

其涉及到的类还有Looper，MessageQueue，Message 等。

其中MessageQueue是事件驱动的基础，本文会重点分析MessageQueue，其他内容会简单带过，可以参考生产者-消费者模式。



参考资料

1、深入理解 MessageQueue

https://juejin.im/entry/6844903476711915534