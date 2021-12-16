---
title: Linux系统之mkbootimg命令
date: 2021-12-15 10:50:25
tags:
	- Linux

---

--

Android 产品中，内核格式是[Linux](https://so.csdn.net/so/search?from=pc_blog_highlight&q=Linux)标准的zImage，

根文件系统采用ramdisk格式。

这两者在Android下是直接合并在一起取名为boot.img,

会放在一个独立分区当中。

这个分区格式是Android自行制定的格式。



参考资料

1、mkbootimg 打包 特殊参数sencond 说明（爬坑系列）

https://blog.csdn.net/Nyiragongo/article/details/103254684