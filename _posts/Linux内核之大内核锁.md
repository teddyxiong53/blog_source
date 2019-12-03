---
title: Linux内核之大内核锁
date: 2019-12-03 10:08:32
tags:
	- Linux

---

1

大内核锁，Big Kernel Lock。是内核开发者在对smp的同步还没有十足的把握的时候，引入的大粒度锁。

简称BLK。

BLK的最初实现是靠一个全局spinlock。

但是大家觉得这个锁的开销太大了，影响了实时性。因此把spinlock改成了mutex。

但是阻塞的时间一般不是很长，所以加锁失败的挂起和唤醒也是非常耗时的，所以又改回了spinlock。

BLK一般是在文件系统、驱动里用得多，目前内核开发者在全力去掉这个锁。





参考资料

1、

https://blog.csdn.net/chenyu105/article/details/7726492