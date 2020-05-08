---
title: cpp之atomic_flag
date: 2018-10-15 15:46:51
tags:
	- cpp

---



atomic_flag是一种简单的原子布尔类型。只支持两种操作：test_and_set和clear。



std::atomic_flag可用于多线程之间的同步操作，类似于linux中的信号量。**使用atomic_flag可实现mutex.**

std::atomic对int, char, bool等数据结构进行原子性封装，在多线程环境中，对std::atomic对象的访问不会造成竞争-冒险。**利用std::atomic可实现数据结构的无锁设计。**



# 参考资料

1、C++11 并发指南六(atomic 类型详解一 atomic_flag 介绍)

https://www.cnblogs.com/haippy/p/3252056.html

2、c++11新特性之atomic

https://www.cnblogs.com/taiyang-li/p/5914331.html