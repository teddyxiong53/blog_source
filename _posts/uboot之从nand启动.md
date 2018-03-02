---
title: uboot之从nand启动
date: 2018-03-01 22:00:36
tags:
	- uboot

---



S3C2410的板子如果被配置为从nand启动，S3C2410的nand Flash controller有个特殊的功能，在板子上电后，CPU 的Nand Flash Controller会自动把Nand上前4K的数据搬运到内部的4K的SRAM，并且把0x0这个地址指向这个内部SRAM，然后开始执行，这个过程，软件不可见。

程序员需要做的，就是在前面4K里，把需要做的事情做了。



# nand flash为什么不能像nor flash那样片内执行程序呢？

1、nand flash是连接到控制器上，而不是系统总线上。

