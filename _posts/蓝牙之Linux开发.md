---
title: 蓝牙之Linux开发
date: 2018-07-23 22:28:29
tags:
	- 蓝牙

---



bluez的代码基础部分都是由高通的Maxim来完成的。

包括HCI、L2CAP、RFCOMM和基本socket的实现。

还有一部分的代码是由Nokia提供的。

bluez是如何实现协议栈的呢？

分为2个部分：

1、kernel层。

除了底部的硬件层，软件上是从HCI层开始的。

bluez是依托于socket的。

首先创建了一个协议类型PF_BLUETOOTH。

2、应用层。

虽然kernel里已经实现了socket。但是应用层如何用ioctl来进行控制，很不方便，所以bluez就进行了一些封装，提供了一些简单好用的应用层api。



# HCI层

HCI是Host Controller Interface的接口。

通过这一层来跟硬件打交道。



# 参考资料

1、实战Linux Bluetooth编程

https://blog.csdn.net/hanmengaidudu/article/details/17028375

2、linux下蓝牙开发(bluez应用)

https://www.cnblogs.com/liangjf/p/8677563.html

3、用树莓派玩转蓝牙

https://www.cnblogs.com/vamei/p/6753531.html

https://zzk.cnblogs.com/s?t=b&w=%E8%93%9D%E7%89%99Linux%E5%BC%80%E5%8F%91