---
title: memcached学习
date: 2019-03-21 09:48:32
tags:
	- memcached

---

1

看muduo的博客，提到说实现了memcached协议。

我对这个memcached已经经常看到，但是一直没有仔细了解这个东西。现在了解一下。



什么是memcached？

是一个分布式的内存对象缓存系统。

是基于key-value的内存存储。

这些数据可以是数据库调用、api调用或者页面渲染的结果。



主要的用途是通过缓存数据库查询结果，减少数据库的访问次数，提高动态web应用的速度。



参考资料

1、Memcached 教程

http://www.runoob.com/memcached/memcached-tutorial.html

2、Memcached使用总结之：Memcache知识点梳理

https://blog.csdn.net/eric_sunah/article/details/51612316