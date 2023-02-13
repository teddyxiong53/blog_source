---
title: glibc辅助运行库分析
date: 2016-12-29 22:09:22
tags:
	- glibc
	- crt0.o
---


我们用c语言写一个程序，入口是main函数，

那么这个main函数是被谁调用了呢？

就是crt0.o的`_start`调用了main函数。

`_start`是真正的入口函数。

你可以自己写汇编文件，入口就写成`_start`。

crt是C RunTime的缩写。

之前的crt0.o包含了很多的东西，

现在已经被拆分成5个文件：crt1.o、crti.o、crtbegin.o、crtend.o、crtn.o。

前面这5个目标文件的作用分别是启动、初始化、构造、析构和结束，它们通常会被自动链接到应用程序中。



假设我们的c程序名字叫test.c，编译的o文件叫test.o。

那么连接的过程是这样的：

先链接crt1.o、crti.o、crtbegin.o。

再链接我们的test.o。

再链接crtend.o、crtn.o。

最后链接用到的库。



# -nostdlib

如果不进行标准的链接的话（编译选项-nostdlib），我们就必须指明这些必要的目标文件，

如果未指定，链接器就会提示找不到_start符号，并因此导致链接失败。



编译时加上选项(-nostdlib)

 

-nostdlib
不连接系统标准启动文件和标准库文件，只把指定的文件传递给连接器。

**这个选项常用于编译内核、bootloader等程序，它们不需要启动文件、标准库文件。**



C语言程序执行的第一条指令。并不是main函数。生成一个C程序的可执行文件时编译器通常会在我们的代码上加上几个被称为启动文件的代crt1.o,crti.o,crtend.o,crtn.o等，他们是标准库文件。这些代码设置C程序的堆栈等，然后调用main函数。他们依赖于操作系统，在裸板上无法执行，所以我们自己写一个。

**所以，我们自己写的*.S汇编文件就是一个启动文件，它设置好堆栈后调用main函数。因此，我们不需要系统自带的启动文件。**

# crt0.o的实现

可以看musl库的实现，这个比较简单。

crt\crt1.c

# 参考资料

1、 crti.o

https://www.cnblogs.com/xpylovely/p/11412380.html

2、ARM-LINUX-GCC -NOSTDLIB

http://blog.chinaunix.net/uid-26739173-id-3154722.html