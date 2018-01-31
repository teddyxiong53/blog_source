---
title: Linux之进程相关各种id
date: 2018-01-31 13:41:22
tags:
	- Linux

---



先从pid说起，pid是讨论的开端。

# pid

pid，进程id，在系统中有唯一性。

但是，pid是可以被回收利用的。当一个进程结束就，它的pid就空出来了。但是这个pid不会马上就分给新的进程。会冷却一下。叫做延迟复用算法。

这个可以避免被其他进程把新进程误认为是老的进程。

pid为0的，叫做调度进程。是主要负责内存换页的。是内核的一部分。

pid为1的，就是大名鼎鼎的init进程。所有用户进程的祖先。init进程一定不会终止。init进程是root权限的。init会收养所有的孤儿进程。



# uid和gid

uid，用户id。

gid，组id。

还配套了有效用户id（euid），有效组id（egid）。

一般情况下，

euid == uid

egid == gid。

