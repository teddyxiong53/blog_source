---
title: Linux之pstore文件系统
date: 2020-04-10 17:46:51
tags:
	- Linux

---



pstore就是persistent store。是一种ramfs。

最初是给non-volatile storage的设备使用。用来debug system crash。

存储的是kernel panic/oops日志。

后面引入了ramoops作为backend。加入了存储kernel console log。

在内核的配置项是：CONFIG_PSTORE。



参考资料

1、pstore/ramoops overview

http://tjtech.me/analyze-pstore-ramoops-in-android-kernel.html