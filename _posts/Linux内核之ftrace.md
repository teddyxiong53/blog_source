---
title: Linux内核之ftrace
date: 2018-03-26 16:41:01
tags:
	- Linux内核

---



把Tracer里的所有内容勾选，则编译非常慢。卡到不能动。

去掉大部分，只剩下最上面的2个，再编译。

还是很慢。把tracer都关闭。再看。就快了很多。看来就是那个tracer的影响。



#参考资料

1、使用 ftrace 调试 Linux 内核

https://blog.csdn.net/adaptiver/article/details/7930646

2、ftrace 简介

https://www.cnblogs.com/danxi/p/6417828.html