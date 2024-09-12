---
title: arm之flush cache
date: 2020-07-24 12:02:51
tags:
	- arm

---



在驱动程序的设计中，我们可能会用到flush_cache_all将ARM cache的内容刷新到RAM，这是因为ARM Linux中cache一般会被设定为write back的。

实际上就是操作cp15协处理器，把cache内容设置为invalid就好了。



参考资料

1、Linux Kernel之flush_cache_all在ARM平台下是如何实现的

https://blog.csdn.net/u011461299/article/details/10199989

