---
title: Linux驱动之为什么使用ioremap
date: 2018-04-09 10:05:32
tags:
	- Linux驱动

---



为什么驱动里读写soc的寄存器的时候，需要用ioremap来拿到虚拟地址再操作呢？

因为这个时候已经打开mmu了。不能直接访问物理地址了。

