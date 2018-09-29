---
title: Linux之后台运行
date: 2018-09-22 22:48:51
tags:
	- Linux

---



我们经常碰到这种问题，在远程登录到linux服务器后，运行一些长时间的任务，但是因为网络不稳定，导致telnet连接断掉了，从而导致任务执行失败。

怎样避免这种情况呢？

有三种方式：

1、nohup。

2、setsid

3、&



nohup是最简单的方式。

hup是hangup的缩写，nohup就是no hangup的意思。

hangup是挂起的意思。

来源是这样的：

在unix的早期版本里，每个终端都通过modem和系统通信，当用户logout的时候，modem就会挂断（hangup）电话。hangup信息就会关闭所有子进程。

所以，解决方式就是：

当前用户注销或者网络断开时，终端会收到hup信号从而关闭所有子进程。

我们的解决途径有两种方法：

1、让进程忽略hup信号。

2、让进程运行在新的会话，从而成为不属于此终端的子进程。



nohup就是第一种方式。

而setsid就属于第二种。



# 参考资料

1、linux进程后台运行方法nohup、setsid、&介绍

https://blog.csdn.net/tanga842428/article/details/62238363