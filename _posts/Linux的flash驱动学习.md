---
title: Linux的flash驱动学习
date: 2017-05-03 20:16:48
tags:
	- Linux
	- flash
typora-root-url: ..\
---

Linux里通过MTD系统来实现对flash的统一操作。其设计框架如下图所示：

![](/images/linux_mtd.jpg)

从上面图中，可以看出基于mtd的Linux flash驱动，可以分为4层：

* 硬件驱动层。nor flash的驱动在`drivers/mtd/chips`目录下，nand flash的驱动在`drivers/mtd/nand`目录下。


* mtd原始设备层。


* mtd设备层。


* 设备节点。mtd字符设备节点主设备号是90，mtd块设备节点的主设备号的31。

用于描述mtd原始设备的结构体是`mtd_info`。

里面定义了一下操作函数。mtd_info对应的物理意义是：假如你有两个mtd设备，每个设备上有3个分区，那么在你的系统中将有6个mtd_info结构体，也就是说，一个分区对应一个mtd_info结构体。



