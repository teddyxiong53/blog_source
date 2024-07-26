---
title: Linux之本地socket使用
date: 2019-07-04 10:39:37
tags:
	- Linux
---

--

# 基本信息

对于本机上的进程间通信，用unix domain socket是比较好的方式。

看看如何进行使用。

unix domain socket是在socket架构的基础上做的一套进程间通信机制。

不需要经过协议栈，只是把一个进程的数据拷贝到另外一个进程。

有SOCKET_DGRAM和SOCKET_STREAM两种模式，对于普通socket的udp和tcp。

unix domain socket是目前最常用的进程间通信方式。X window就是用的这种通信方式。

直接看例子。

代码放在这里了。很简单。

https://github.com/teddyxiong53/c_code/tree/master/linux/socket/unix_domain

# 同一个unix socket可以多次打开吗？

在 Unix 系统中，同一个 Unix 域套接字（Unix domain socket）可以被多个进程或者线程同时打开和使用。多个进程或线程可以通过打开同一个 Unix 域套接字来进行通信。这种方式与网络套接字（TCP、UDP）不同，网络套接字需要绑定到不同的端口号以区分不同的连接，而 Unix 域套接字是基于文件系统路径的，因此可以在同一个路径上打开多个套接字。

多个进程或线程可以同时连接到同一个 Unix 域套接字来进行通信，这种情况下需要注意以下几点：

1. **并发访问**：多个进程或线程可以同时向同一个 Unix 域套接字写入和读取数据。这种并发访问需要适当的同步机制，以避免数据竞争和混乱。

2. **消息边界**：与 TCP 不同，Unix 域套接字传输的数据没有消息边界，因此需要应用层协议来区分不同的消息。

3. **权限控制**：通过文件系统权限控制可以限制对 Unix 域套接字的访问，确保只有授权的进程或者用户可以连接和通信。

4. **关闭套接字**：当不再需要使用 Unix 域套接字时，需要及时关闭套接字以释放资源。

总的来说，Unix 域套接字可以被多个进程或者线程同时打开和使用，但需要注意并发访问和数据同步的问题，以确保通信的正确性和可靠性。

# 参考资料

1、UNIX SOCKET简介

https://blog.csdn.net/zhangkun2609/article/details/84188465