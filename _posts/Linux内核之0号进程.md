---
title: Linux内核之0号进程
date: 2019-12-05 09:47:28
tags:
	- Linux
---

1

Linux 里有3个特殊的进程：

idle进程（pid=0）

init进程（pid=1）

kthreadd（pid=2）

# idle进程

idle进程又系统自动创建，运行在内核态。

idle进程是唯一一个没有通过fork或者kthread创建的进程。

完成系统加载后，变成进程调度、交换。



0号进程的前世是init_task，今生是idle。



在smp系统上，每个核心有独立的运行队列。每个运行队列上有一个idle进程。



init_task是内核中所有的进程、线程的task_struct的雏形。



参考资料

1、linux的 0号进程 和 1 号进程

https://www.cnblogs.com/alantu2018/p/8526970.html