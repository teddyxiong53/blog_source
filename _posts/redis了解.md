---
title: redis了解
date: 2019-08-23 09:29:03
tags:
	- redis
---

1

因为访问数据库是比较耗时的。而有很多场景下，各个用户查询的信息是一样的。没有必要每个人都去查询数据库。只需要第一次查询出来，把内容缓存到内存里，后面的用户就直接使用缓存的内容。

这个缓存，之前就是memcached。

memcached采用了客户端+服务端的架构方式。

只要遵循协议，使用什么语言实现都可以的。

memcached使用slab的内存管理算法。可以减少内存的碎片和频繁分配销毁的开销。

# mysql + memcached架构存在的问题

1、mysql需要不断进行拆库和拆表的操作。memcached也需要跟着不断扩容。这个导致维护工作非常困难。

2、memcached和mysql数据一致性的问题。

3、memcached数据命中率低或者重启后，大量的访问直接穿透到数据库，mysql无法支撑。

4、跨机房的cache同步问题。







参考资料

1、Redis应用场景

https://blog.csdn.net/hguisu/article/details/8836819