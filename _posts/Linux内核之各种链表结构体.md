---
title: Linux内核之各种链表结构体
date: 2018-04-08 20:40:58
tags:
	- Linux内核

---



在内核里，我们一般看到的就是struct list_head这种链表。是双向循环链表，实现简单，功能强大。

但是在内核里，还存在着其他两种重要的链表。我们现在就分析一下。

另外两种链表，一种是struct hlist。h代表的是hash。这种实现上有点绕。大家都不太习惯。

另外一种是klist。

klist也是为了适应某种特殊的情形。主要用在设备驱动模型里。为了适应动态变化的驱动和设备，而专门设计的。



# 参考资料

1、linux内核部件分析（四）——更强的链表klist

https://blog.csdn.net/qb_2008/article/details/6845854