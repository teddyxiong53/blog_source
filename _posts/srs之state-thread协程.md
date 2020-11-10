---
title: srs之state-thread协程
date: 2020-11-06 11:12:30
tags:
	- 直播
---

1

协程是一种程序组件，也叫微线程。

一般我们把协程理解为自己实现调度，用于提高程序运行效率，降低开发复杂度的微线程。

协程在用户态实现调度。

而普通的线程的调度，需要切换到内核态。

协程这样就减少了换页操作，提高了效率。

开发者可以用同步的方式去进行代码开发。不需要考虑多线程开发的资源保护问题。



协程在处理异步等待事件的时候，有很大的优势。

例如io读写一般比较耗时，cpu在遇到io读写的时候，需要切换线程。

使用协程就可以直接在用户切换微线程。





state threads

协程库state threads library(以下简称st)是一个基于setjmp/longjmp实现的C语言版用户线程库或协程库（user level thread）。



基于setjmp和longjmp实现协程库基本步骤（下述线程指用户线程）：

1.需要用jmpbuf变量保存每一个线程的运行时环境，称为线程上下文context。

2.为每个线程分配（malloc/mmap）一个stack，用于该线程运行时栈，该stack完全等效于普通系统线程的函数调用栈。**该stack地址是在线程初始化时设置，所以不需要考虑setjmp时保存线程的栈上frames数据的问题。**

3.通过调用setjmp初始化线程运行时上下文，将context数据存放到jmpbuf结构中。然后修改其中的栈指针sp指向上一步分配的stack。根据当前系统栈的增长方向，将sp设置为stack的最低或最高地址。

4.线程退出时，需要返回到一个安全的系统位置。即，需要有一个主线程main thread或idle thread来作为其他线程最终的退出跳转地址。需要为主线程保存一个jmpbuf。

5.设置过main thread的jmpbuf后，需要跳转到其他线程开始执行业务线程。

6.实现一个context交换函数，在多个线程之间进行跳转：保存自己的jmpbuf，longjmp到另一个线程的jmpbuf。



参考资料

1、srs之state thread库接口分析

https://segmentfault.com/a/1190000019539131

2、协程库st(state threads library)原理解析

https://www.cnblogs.com/NerdWill/p/6166220.html

3、使用State Threads实现简单的服务器

https://blog.csdn.net/caoshangpa/article/details/79582873