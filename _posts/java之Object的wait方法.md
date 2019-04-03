---
title: java之Object的wait方法
date: 2019-04-02 17:52:04
tags:
	- java

---





Object里为什么会有wait和notify方法？做什么用的？

wait、notify、notifyAll。这3个函数是native的，而且是final的，所以所有Object的子类的行为都是一样的。

有三种方式调用，效果完全一样：

```
wait();
this.wait();
super.wait();
```

这3个方法，是为了配合syncronized关键字的工作的。

这个就是为了实现java里的对象锁。



参考资料

1、Object.wait()与Object.notify()的用法

https://www.cnblogs.com/xwdreamer/archive/2012/05/12/2496843.html

2、Java线程同步 （synchronized wait notify）

https://blog.csdn.net/weizhaozhe/article/details/3922647

3、Java线程锁，synchronized、wait、notify详解

http://www.cnblogs.com/LeeScofiled/p/7225562.html