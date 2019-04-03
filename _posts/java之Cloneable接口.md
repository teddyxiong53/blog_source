---
title: java之Cloneable接口
date: 2019-04-03 11:08:04
tags:
	- java

---



什么是clone？

就是在heap上克隆出一个和原对象一模一样的对象，并把这个对象的地址赋值给新的引用。

一个类要实现clone功能，就需要实现Cloneable接口。

否则会出现CloneNotSupportedException。



参考资料

1、Java中 Cloneable 、Serializable 接口详解

https://blog.csdn.net/xiaomingdetianxia/article/details/74453033