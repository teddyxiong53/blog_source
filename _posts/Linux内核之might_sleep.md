---
title: Linux内核之might_sleep
date: 2020-08-29 14:55:25
tags:
	- Linux

---

1

*might_sleep():* 指示当前函数可以睡眠。

如果它所在的函数处于原子上下文*(atomic context)*中*(*如，*spinlock, irq-handler…)*，将打印出堆栈的回溯信息。

**这个函数主要用来做调试工作，**在你不确定不期望睡眠的地方是否真的不会睡眠时，就把这个宏加进去。

参考资料

1、

https://blog.csdn.net/freeandperson/article/details/84426031