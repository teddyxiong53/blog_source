---
title: 蓝牙之C语言编程
date: 2018-12-12 10:55:35
tags:
	- 蓝牙

---



还是用C语言编程，更加接近事物的本质。

有一个usb蓝牙适配器，怎么用C语言写一个程序，把适配器用起来呢？

有个《实战Linux Bluetooth编程 》系列文章可以看一下。用谷歌搜索一篇篇看吧。



bluez由两部分构成：

1、kernel部分。软件上从HCI层开始实现就可以了。底层的硬件已经实现了。

2、应用层部分。如果不封装一些库，那就只能socket编程。这样还是很麻烦的。



bluez是通过dbus跟其他应用程序通信的。

bluez和dbus的结合，跟桌面系统提供了完美的组合。



# HCI层编程

bluez也给我们封装了hci的相关接口。

直接基于socket的话，就是新建一个socket，类型是BTPROTO_HCI



# 参考资料

1、bluez-experiments

https://github.com/carsonmcdonald/bluez-experiments

2、实战Linux Bluetooth编程（二） BlueZ简介

http://blog.sina.com.cn/s/blog_602f87700100e57t.html