---
title: 嵌入式之newlib了解
date: 2018-02-05 23:43:37
tags:
	- 嵌入式
	- libc

---



官网在这里：http://sourceware.org/newlib/。

由红帽公司来维护。

newlib主要是针对嵌入式场景进行优化。由libc和libm这2个库组成。特点是轻量级，速度快，适配了很多的CPU。

在普通pc上的使用方法是：gcc带上`--with-newlib`选项。

