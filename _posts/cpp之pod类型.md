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

1、没有虚函数，没有虚继承。

就类型C语言里的struct。



Trivial平凡类型。



平凡类型的定义



# 参考资料

1、C++11：POD数据类型

https://blog.csdn.net/aqtata/article/details/35618709

2、C++11中的POD和Trivial

https://blog.csdn.net/dashuniuniu/article/details/50042341