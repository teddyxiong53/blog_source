---
title: cpp之定时器实现
date: 2020-05-25 16:24:08
tags:
	- cpp

---

1

现在需要实现闹钟的功能，需要实现定时操作。

java里有Timer类，可以实现定时操作功能。

c++里应该怎么做比较好呢？

网上找了一下，没有看到什么好的方案，那就从muduo里扒出定时器相关代码来用。

这个的本质是Linux的timerfd的使用。

muduo里引入，还是会带入不少我并不需要的东西。

我还是自己用timerfd加select自己来实现一个简单的。



或者最简单的方式：

直接写一个线程进行定时检查？



参考资料

1、C++定时器功能实现

https://blog.csdn.net/Fallinlove520/article/details/93131930

2、c++11实现异步定时器

https://www.cnblogs.com/gtarcoder/p/4924097.html