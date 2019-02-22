---
title: cpp之pod类型
date: 2018-10-11 18:32:51
tags:
	- cpp
---



POD，是Plain Old Data的缩写。中文翻译为：平凡的老旧的数据格式。

表示c++里的某种数据类型。

通俗来说，一个类或者结构体在经过二进制拷贝后，还能保持其数据不变。那么它就是一个POD类型。

为什么需要POD？POD是c++为了兼容C 的内存布局而设计的。主要用于修饰用户自定义的类型。

POD的内涵是什么？

在c++03里，是这样要求的：

```
1、没有虚函数，没有虚继承。
2、可以被静态初始化。
```

就类似C语言里的struct。而且不能有成员函数。

加了成员函数，即使内存布局仍然跟C语言是兼容的，但是也不再是一个POD了。

c++11放宽了这种限制。

把POD分为两种：

```
1、平凡的Trivial。
2、标准布局standard-layout。
```

一个平凡的类型可以用memcpy来进行复制。

平凡的类型，它的生命周期开始于空间被分配时，而不是构造函数完成时。











# 参考资料

1、C++11：POD数据类型

https://blog.csdn.net/aqtata/article/details/35618709

2、C++11中的POD和Trivial

https://blog.csdn.net/dashuniuniu/article/details/50042341

3、

https://zh.wikipedia.org/wiki/C%2B%2B11