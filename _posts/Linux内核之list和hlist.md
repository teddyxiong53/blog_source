---
title: Linux内核之list和hlist
date: 2021-03-04 17:57:51
tags:
	- Linux

---

--

hlist也是 一种双向链表，

但不同于list_head，

它的头部只有一个指针，

常被用作哈希表的bucket数组，这样就可减少哈希bucket一半的内存消耗。



参考资料

1、

https://www.cnblogs.com/x_wukong/p/8506894.html