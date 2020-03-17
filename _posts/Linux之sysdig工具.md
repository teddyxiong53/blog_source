---
title: Linux之sysdig工具
date: 2020-03-14 14:12:28
tags:
	- Linux

---

1

sysdig的定位是：

1、系统监控。

2、分析和故障排查工具。

# 为什么需要sysdig

在sysdig之前，Linux已经有很多的系统监控类的工具，例如strace、tcpdump、lsof等。

那为什么还需要sysdig？它做了什么有价值的工作？

可以用3个关键字来概括：整合、强大、灵活。

先说整合。

之前说的那些工具，都是分散的，每个工具实现一个功能，它们之间的数据不能相通，分析使用比较麻烦。sysdig的价值之一在于整合了多个功能。提供了一站式的使用体验。

再说强大。

sysdig可以获取实时的系统数据，并把数据保存到文件里，供后续分析用。

再说灵活。

sysdig有这类似tcpdump的过滤语法。还可以自己用lua来编写过滤逻辑。



# sysdig是怎样工作的

向内核系统调用注册hook。

当系统调用完成的时候，它会把信息拷贝到特定的buffer。然后整理压缩过滤。

最后通过sysdig命令行工具进行交互。







参考资料

1、使用 sysdig 进行监控和调试 linux 机器

https://cizixs.com/2017/04/27/sysdig-for-linux-system-monitor-and-analysis/