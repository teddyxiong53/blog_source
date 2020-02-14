---
title: Linux内核之idr分析
date: 2019-12-09 13:58:38
tags:
	 - Linux

---

1

从本质上来说，这就是**一种将整数ID号和特定指针关联在一起的机制**。

这个机制最早是在2003年2月加入内核的，当时是作为POSIX定时器的一个补丁。现在，在内核的很多地方都可以找到idr的身影。

遇到这种清况，我们就可以采用idr机制，该机制内部采用radix树实现，可以很方便地将整数和指针关联起来，并且具有很高的搜索效率。



参考资料

1、浅析linux内核中的idr机制

https://blog.csdn.net/ganggexiongqi/article/details/6737389

2、linux中的IDR机制

https://blog.csdn.net/midion9/article/details/50923095