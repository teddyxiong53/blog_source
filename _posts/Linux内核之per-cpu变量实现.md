---
title: Linux内核之per-cpu变量实现
date: 2018-04-07 20:27:24
tags:
	- Linux

---



Linux内核里，为了提高smp系统的性能，加入了per-cpu变量的机制。

用来给每个CPU都生成一个变量的副本，从而不需要加锁，达到提高性能的目的。



# 静态per-cpu变量

这个是用DEFINE_PER_CPU来定义的。

跟普通变量的区别就是，per-cpu变量放在一个特殊的section里。

# 动态per-cpu变量

用的是alloc_percpu函数。



