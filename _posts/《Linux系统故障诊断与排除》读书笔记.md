---
title: 《Linux系统故障诊断与排除》读书笔记
date: 2017-06-07 22:07:13
tags:

	- Linux

	- 读书笔记

---

最近看公司的一个文档，看到末尾写的引用文档里，有三本书，分别是：

《Debug Hacks 深入调试的技术和工具》

《Linux系统故障诊断与排除》

《精通Linux内核必会的75个绝技》

所以就找到这3本书的pdf版本，学习记录下来。很多的知识点会独立成文章。



# 1. 内容概述

《Debug Hacks》该书主要讲应用程序和内核的调试方法。



# 2. coredump的一些知识

## 2.1 压缩core文件

可以写一个脚本，名字叫做`/usr/local/sbin/core_helper`内容如下：

```
#!/bin/sh
exec gzip - > /var/core/$1-$2-$3-$4.core.gz
```

然后把kernel的core_pattern改为`|/usr/local/sbin/core_helper %t %e %p %c`。注意管道符。



## 2.2 使用内核转储掩码排除共享内存

大规模的应用程序一般会使用多进程，这些进程直接回共享多大几个G的内存。这种应用程序在发生内核转储的时候，所有进程的共享内存全部转储的话，会占用大量的磁盘空间，无疑不妥当。而且共享内存的内容是相同的，没有必要再每个进程里都放一份的。Linux考虑到了这一点，你可以设置只让某个进程（例如主进程）对共享内存进行转储，其他进程不不用存了。

方法很简单，就是设置`/proc/PID/coredump_pattern`的值。









