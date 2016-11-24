---
title: linux socket相关函数从应用层到驱动层分析
date: 2016-11-02 21:57:01
tags:
	- linux
---
以DM9000的驱动为例，分析一个简单tcp服务器端程序，在进行listen并select后，有客户端连接过来时，linux系统的处理过程。把其中涉及到的知识点都分析一下。
首先想要了解的是，select时，select函数是如何跟内核内部的调度和驱动进行挂钩的。
按照我当前的理解，select函数会让当前进程进入到睡眠状态，我当前的select会监听readfdset，而一旦有数据到达驱动，驱动会产生消息，系统得到这个消息，然后把进行select的进程唤醒。大概是这么个流程，但是代码是如何写的。下面就顺着函数来看看。
linux 2.6版本应该是跟当前最新版本差别没那么巨大，很多东西都还是相同的。这个版本的代码量也没那么大，所以我就以这个版本来分析。我选择的是2.6.35.7，选这个的版本是因为我刚好有这个版本。
select函数在fs/select.c里。
select是一个系统调用，linux里定义系统调用都是用`SYSCALL_DEFINE5`这样来定义，最后拿个5是表示这个调用的参数个数是5个。
```
SYSCALL_DEFINE5(select, int, n, fd_set __user *, inp, fd_set __user *, outp,
		fd_set __user *, exp, struct timeval __user *, tvp)
```
在这里，我们可以看到几个点需要理解一下：
1. `__user`代表什么含义？
在`include/linux/compiler.h`里，有这个定义：
```
#ifdef __CHECKER__
# define __user		__attribute__((noderef, address_space(1)))
# define __kernel	__attribute__((address_space(0)))
```
`__attribute__`这个是gnu c扩展的c语言特性，用来指定变量和函数的属性。
`noderef`这个只有linux源代码才用到了，不是gcc相关的，是调用了外部程序sparse做的检查。
在linux的源代码根目录的Makefile里有这样的注释。
```
# Call a source code checker (by default, "sparse") as part of the
# C compilation.
#
# Use 'make C=1' to enable checking of only re-compiled files.
# Use 'make C=2' to enable checking of *all* source files, regardless
# of whether they are re-compiled or not.
#
# See the file "Documentation/sparse.txt" for more details, including
# where to get the "sparse" utility.
```
---
sparse简介
sparse诞生于2004年，是Linus的作品（好吧，真有你的，大神）。
这个是一个静态的代码检查工具，用来减少内核代码里的隐患。
在之前，用的是swat，这个工具不是免费的，所以Linus就自己写了sparse。这个套路是不是很眼熟，git的诞生也是因为之前用的版本管理工具要收费了，Linus自己写的。大神从来都是自己动手，丰衣足食啊。
在内核代码的Document/sparse.txt里，有一些介绍。
sparse通过gcc的扩展属性`__attribute__`和自己定义的`__context__`来对代码进行静态检查。
下面罗列一些基本的定义。
```
宏名字                     宏定义                                               作用
__bitwise                 __attribute__((bitwise))                             确保变量的大小端模式统一
__user                    __attribute__((noderef, address_space(1)))           指针地址必须在用户空间
__kernel                  __attribute__((address_space(0)))                    指针地址必须在内核空间。
__iomem                   __attribute__((noderef, address_space(2)))           指针地址必须在设备地址空间。
```
---
我们继续回到select的源代码往下阅读。

