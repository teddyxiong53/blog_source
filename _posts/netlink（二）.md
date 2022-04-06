---
title: netlink（二）
date: 2018-04-03 16:10:48
tags:
	- netlink

---



新的linux内核使用udev代替hotplug来做热插拔管理。

但是我们还是有很多情况下需要在应用里自己检测热插拔，例如在读写SD卡的时候，拔掉SD卡，那么就需要马上检测出这种情况，停止读写，防止vfs崩溃。



netlink是面向数据包的服务。为内核和用户之间搭建了一个高速通道。是udev实现的基础。

这种方式是异步的，不需要轮询等待。

监听这种消息就好了。NETLINK_KOBJECT_UEVENT



# 参考资料

1、Netlink实现热拔插监控

http://blog.chinaunix.net/uid-24943863-id-3223000.html

