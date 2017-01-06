---
title: glibc辅助运行库分析
date: 2016-12-29 22:09:22
tags:
	- glibc
	- crt0.o
---
我们用c语言写一个程序，入口是main函数，那么这个main函数是被谁调用了呢？就是crt0.o的`_start`调用了main函数。`_start`是真正的入口函数。你可以自己写汇编文件，入口就写成`_start`。
crt是C RunTime的缩写。
之前的crt0.o包含了很多的东西，现在已经被拆分成5个文件：crt1.o、crti.o、crtbegin.o、crtend.o、crtn.o。
假设我们的c程序名字叫test.c，编译的o文件叫test.o。那么连接的过程是这样的：
先链接crt1.o、crti.o、crtbegin.o。
再链接我们的test.o。
再链接crtend.o、crtn.o。
最后链接用到的库。



