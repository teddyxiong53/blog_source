---
title: Linux的原子操作
date: 2017-04-20 23:32:06
tags:
---
Linux的原子操作
1、Linux对原子操作的支持，包括两种类型：位和整数。
2、提供了atomic_t类型，就是一个结构体，里面就是一个int类型变量。
3、提供了操作函数atomic_add、atomic_sub等。实现原理就是锁中断。
4、针对bit的操作函数有：test_bit、test_and_set_bit等。
看看内核锁的实现.其关键基本都是lock实现原子操作
Linux原子操作问题来源于中断、进程的抢占以及多核smp系统中程序的并发执行。
