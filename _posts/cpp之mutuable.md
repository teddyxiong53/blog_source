---
title: cpp之mutuable
date: 2019-03-25 14:15:32
tags:
	- cpp

---



1

mutuable字面含义是可变的。

既然是可变的，那么就不能修饰函数或者类了。

既然强调可变，那么修饰的对象就不应该是变量，因为变量本来就是可变的。

那么mutuable是干啥用的？

是用来修饰类的成员变量，这样修饰的成员变量，可以在const尾部修饰的函数里进行修改。

主要就是修饰mutex这种用的。



参考资料

1、C++ 中的 mutable 关键字

https://liam.page/2017/05/25/the-mutable-keyword-in-Cxx/