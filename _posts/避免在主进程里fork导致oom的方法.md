---
title: 避免在主进程里fork导致oom的方法
date: 2017-05-07 19:10:47
tags:

	- linux

---

有时候需要在C代码里去调用脚本做一些事情，但是因为Linux下的fork机制，会让子进程分配同样多的内存，这就会导致有时候出现oom的错误。怎么解决呢？

一个简单可行的办法，就是另外起一个进程，在这个进程专门用来进行system函数调用，而这个进程本来不占用太多内存。

用mqueue就可以实现。具体看我的github代码：`https://github.com/teddyxiong53/c_code/tree/master/linux/mqueue`。

