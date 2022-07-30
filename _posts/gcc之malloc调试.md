---
title: gcc之malloc调试
date: 2022-07-29 14:23:07
tags:
	- gcc

---

--

我现在是有个问题，在malloc要么是出现段错误，要么是失败。

其实内存是有非常多的。

为什么会出现这种问题，怎么进行调试？

对malloc和free进行wrap操作就可以了。

我另外有篇文章说了这个问题了。



参考资料

1、

https://www.cnblogs.com/arnoldlu/p/10827884.html

2、

https://www.cnblogs.com/arnoldlu/p/9649229.html#valgrind