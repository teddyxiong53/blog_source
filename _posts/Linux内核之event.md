---
title: Linux内核之event
date: 2018-04-03 15:58:25
tags:
	- Linux内核

---



内核事件层实现了内核到用户的消息通知系统。

是基于kobject来实现的。

系统需要一种机制，来帮助内核把事件输出到用户空间，这一点对于桌面系统尤其重要。

例如，磁盘满了、插入U盘了等等。

早期的事件层没有采用kobject和sysfs，都没有存在多久就被淘汰了。

现在的事件层借助于kobject和sysfs，是非常好的。

内核事件层把事件模拟为信号。从一个kobject出发，所以每个事件源都是一个sysfs路径。

如果请求的事件跟你的第一个硬盘相关，那么/sys/block/hda就是源树。

每个事件都有一个可选的payload。

这个payload一般是sysfs的attribute。

从内部实现上讲，从内核空间传递事件到用户空间，用的是netlink。

在桌面系统上，有一个标准，就是dbus。实现对netlink事件的监听，