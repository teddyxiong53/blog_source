---
title: Linux内核之1号进程
date: 2018-03-13 16:29:33
tags:
	- Linux

---



Linux里有3个特殊进程：

1、idle进程，pid为0 。

2、init进程。pid为1 。

3、kthreadd。pid为2 。

这个过程可以用道生一，一生二，二生三，三生万物来描述。

道生一：系统生成idle进程。

一生三：idle生成init和kthreadd

二生三：这个有点牵强，这句略过。

三生万物：init生成所有的用户进程。kthreadd产生所有的内核线程。



idle进程是由系统创建的第一个进程，也是唯一一个没有通过fork或者kernel_thread来创建的进程。

在系统完成启动后，idle负责在后台进行进程调度和换页。

idle进程是所有进程（包括内核进程和用户进程）的祖先。



init进程是idle创建的，是所有的用户进程的祖先。

系统启动完成后，init变成守护进程监视其他进程。

init进程先是一个内核进程，系统启动后，退化为用户进程。



kthreadd是所有其他内核线程的祖先，负责所有内核线程的调度和管理。



# 参考文章

1、Linux下1号进程的前世(kernel_init)今生(init进程)----Linux进程的管理与调度（六）

http://blog.csdn.net/gatieme/article/details/51532804

2、分析Linux内核创建一个新进程的过程

https://www.cnblogs.com/Nancy5104/p/5338062.html