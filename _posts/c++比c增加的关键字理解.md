---
title: cpp比c增加的关键字理解
date: 2016-12-05 20:15:53
tags:
	- cpp
---
cpp相当于c语言，增加了10几个关键字，现在把有疑问的梳理如下。
1. mutable
这个是存储类型相关的关键字。总共有5种类型：auto、register、static、extern、mutable。
对于register类型的变量，不能用`&`来取地址，因为它没有内存地址。用register修饰的变量是尽量存在寄存器里，但是不保证可以存。
mutable修饰符只能用来修饰类对象。


