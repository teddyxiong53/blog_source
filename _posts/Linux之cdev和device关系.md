---
title: Linux之cdev和device关系
date: 2017-08-05 22:27:51
tags:

	- Linux

---

看Linux里struct cdev的定义，按照我的理解，cdev应该是一种特别的device，按道理应该包含一个device的成员变量才对，但是实际上并不是。这个改怎么理解？

cdev和device是如何关联起来的？

可以采用共同拥有的Kobjcet这个成员作为纽带。



Linux下几乎所有的设备都是device的子类，无论是platform设备还是I2C设备还是网络设备。但是唯独cdev不是。这个可以从cdev的结构体定义可以看出，cdev_add也只是把它放到cdev_map里。这个是历史原因造成的。

cdev更适合理解为一种接口，而不是一种设备。