---
title: platform设备驱动分析
date: 2016-11-04 22:30:44
tags:
	-linux驱动
---
1

看DM9000的驱动代码，会发现`platform_driver`这样一些概念，`platform_driver`具体怎么理解呢？它的设计初衷是什么呢？下面就进行分析。

对于I2C、SPI、USB设备而言，设备和驱动都挂接在对应的总线上，但是对于led、以太网这种不依附于总线的设备，设备和驱动如何进行关联呢？内核为此提供了虚拟的总线，platform。我们且称之为平台总线。
相应地，挂接在平台总线上的设备和驱动被称为平台设备`platform_device`和平台驱动`platform_driver`。

平台设备并不是与块设备、字符设备、网络设备并列的概念。



