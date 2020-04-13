---
title: Android系统之AndroidVerifiedBoot（avb）
date: 2020-04-11 09:59:51
tags:
	- Android

---

1

这个就是跟解锁相关的一个概念了。

如果被解锁过，开机会提示设备已经被unlock，不可以被trust。

目的是为了保护系统的安全性。

实现的方式：

在设备启动过程中，无论在哪一个阶段，都会在进入到下一个阶段之前先验证下一阶段的完整性和真实性。





参考资料

1、

https://www.jianshu.com/p/d354280f1f27

2、

https://blog.csdn.net/rikeyone/article/details/80606147

3、

https://blog.csdn.net/weixin_43836778/article/details/90400147