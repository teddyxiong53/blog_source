---
title: cpp之性能分析
date: 2019-11-27 16:07:51
tags:
	- cpp
---

1

c++ 2个最大的性能隐患：

1、临时变量。这个解决方法是，尽量传递引用。

2、隐式转换。这个解决方法是，禁止隐式转换。



heap对象和stack对象

对于java、js这些语言，所有的对象都是在heap里。



参考资料

1、C++ 性能剖析

https://blog.csdn.net/u013279723/article/details/72323545