---
title: Linux驱动之LDD3源代码分析
date: 2018-03-07 22:43:42
tags:
	- Linux

---



LDD3是本经典，但是翻译实在是读不下去。我直接看源代码。看书为辅。

LDD3是基于linux2.6的。比较老了。有人移植了相关例程到linux新版本上，最新已经支持到4.9了。

代码在这里。https://github.com/duxing2007/ldd3-examples-3.x

书的目录结构：

```
1、设备驱动简介
2、建立和运行模块。
3、字符驱动
	scull。实现了这些设备。
		1、scull0到scull3 。
		2、scullpipe0到scullpipe3.
		3、scullsingle
		4、scullpriv
		5、sculluid
		6、scullwuid
		
4、调试技术
5、并发
6、高级字符驱动
7、时间
8、分配内存。
9、操作硬件。
10、中断
11、内核里的数据类型。
12、PCI驱动。
13、usb
14、linux设备模型。
15、内存映射和dma
16、块设备。
17、网络驱动。
18、tty驱动。
```



