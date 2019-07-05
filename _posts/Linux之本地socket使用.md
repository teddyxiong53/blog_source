---
title: Linux之本地socket使用
date: 2019-07-04 10:39:37
tags:
	- Linux
---



对于本机上的进程间通信，用unix domain socket是比较好的方式。

看看如何进行使用。

unix domain socket是在socket架构的基础上做的一套进程间通信机制。

不需要经过协议栈，只是把一个进程的数据拷贝到另外一个进程。

有SOCKET_DGRAM和SOCKET_STREAM两种模式，对于普通socket的udp和tcp。

unix domain socket是目前最常用的进程间通信方式。X window就是用的这种通信方式。

直接看例子。

代码放在这里了。很简单。

https://github.com/teddyxiong53/c_code/tree/master/linux/socket/unix_domain



参考资料

1、UNIX SOCKET简介

https://blog.csdn.net/zhangkun2609/article/details/84188465