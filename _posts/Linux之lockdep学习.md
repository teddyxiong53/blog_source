---
title: Linux之lockdep学习
date: 2018-01-15 16:11:21
tags:
	- Linux
	- 死锁
typora-root-url: ..\

---



Linux提供了检测死锁的机制，就是lockdep。

一般死锁可以分为两种的情况：

1、D状态死锁。这种不会导致看门狗复位。

2、R状态死锁。会导致看门狗复位。

lockdep就是针对R状态死锁的。

一般的错误类型是：

1、AA。重复上锁。

2、ABBA。曾经使用AB的属性上锁，然后又用BA的顺序上锁。

3、ABBCCA。这个是对ABBA的扩展。BBCC相当于中间部分。这种锁人工很难发现。

4、多次Unlock。



死锁会存在于线程或者进程中。下面统一用线程的来进行描述。



# ABBA死锁的形成

thread1和thread2，分别使用了A和B这2把锁。

thread1是先用A再用B，thread2刚好相反。



这个可能在运行中出现的情况，可以用二维的坐标图来描述一下。

![死锁坐标分析](/images/死锁坐标分析.png "死锁坐标分析")



# lockdep死锁检测模块介绍

上面我们讨论是一个简单的锁的情况。而在kernel的代码里，里面有大量的锁，这个如果没有一个好的检测机制，死锁就很难以避免。要尽量早地发现问题才行。

2006年，kernel开始引入了lockdep机制。

原理简单说，就是维护了一个链表进行检查，发现有问题，内核马上panic掉。





# 参考资料

1、

https://blog.csdn.net/lqxandroid2012/article/details/53784323



