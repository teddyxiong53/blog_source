---
title: Linux内核之might_sleep函数
date: 2022-10-17 16:50:33
tags:
	- Linux内核

---

--

对于内核常用的might_sleep函数，如果没有调试的需要(没有定义CONFIG_DEBUG_ATOMIC_SLEEP)，这个宏/函数什么事情都不，might_sleep就是一个空函数，所以平常看code的时候可以忽略。内核只是用它来提醒开发人员，调用该函数的函数可能会sleep。

参考资料

1、

https://blog.csdn.net/m0_47799526/article/details/108113816