---
title: java之原子操作
date: 2019-04-03 10:24:04
tags:
	- java
---



jvm规范里有一条是这么定义的：

````
除了long和double的操作外，对基本类型的操作都是原子级的。
````

就是对于32bit及以下的，可以保证原子性。

对于double的操作，可以用volatile来修饰来做到原子性。



参考资料

1、JAVA之long和double读写操作原子性

https://blog.csdn.net/luoyoub/article/details/80275539

