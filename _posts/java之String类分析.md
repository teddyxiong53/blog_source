---
title: java之String类分析
date: 2017-12-20 21:49:00
tags:
	- java
---





# String和StringBuffer使用区别

1、简单来说，String相当于是一个常量，StringBuffer相当于是一个变量。String对象不可以被修改，如果重新赋值，就是两个对象了。

2、StringBuffer内部实现与String不同，在处理过程中，不生成新的对象。在内存使用上比String要好。如果使用过程中经常对字符串进行插入删除等操作，则使用StringBuffer。



