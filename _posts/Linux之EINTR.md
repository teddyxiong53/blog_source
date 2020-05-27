---
title: Linux之EINTR
date: 2020-05-27 22:46:08
tags:
	- Linux

---

1

什么时候会产生errno为EINTR的错误。

例如：read一直阻塞的时候，这时候本进程收到了一个SIGUSR1（任何一个信号），进程转去处理信号了。read这个系统调用就会返回，但是实际上当前没有东西可读。这个时候，errno就会被设置为EINTR。所以这种错误，我们需要忽略掉它。



参考资料

1、中断产生EINTR错误

https://blog.csdn.net/junlon2006/article/details/80403737