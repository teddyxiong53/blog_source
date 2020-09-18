---
title: Android系统之gralloc
date: 2020-09-15 09:13:32
tags:
	- Android系统

---

1

`gralloc`是Android中负责申请和释放`GraphicBuffer`的HAL层模块，由硬件驱动提供实现，为`BufferQueue`机制提供了基础。`gralloc`分配的图形Buffer是进程间共享的，且根据其Flag支持不同硬件设备的读写。

![img](../images/random_name/16f2cd416731eec8)







参考资料

1、Android图形系统系统篇之Gralloc

https://juejin.im/post/6844904025851166734