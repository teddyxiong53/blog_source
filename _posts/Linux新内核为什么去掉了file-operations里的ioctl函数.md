---
title: Linux新内核为什么去掉了file_operations里的ioctl函数
date: 2017-05-25 23:10:07
tags:

	- Linux

	- ioctl

---

老的Linux驱动在较新的系统上进行编译了，会碰到ioctl成员找不到的错误。这个是为什么呢？

在老的Linux头文件里，file_operations结构体里有3个ioctl函数，分别是`ioctl`,`unlocked_ioctl`,`compat_ioctl`这3个。

新的系统里，**ioctl完全被unlocked_ioctl取代了**。

unlocked_ioctl比ioctl少了一个inode参数。

本质区别是，**unlocked_ioctl不用再上大内核锁了。**

现在总体的方向是kernel开发者在试图移除大内核锁。

那么什么是大内核锁呢？

大内核锁缩写为BKL。

是kernel开发者在他们对SMP系统的同步还没有十足的把握的时候，引入的大粒度锁。

这个锁肯定是会导致性能下降的。



# compat_ioctl

这个是为了64位kernel配合32位应用工作而提供的。

具体实现上，可以直接调用unlocked_ioctl，只需要把最后的参数转换一下。

```
unlocked_ioctl(filp, cmd, (unsigned long)compat_ptr(arg));
```



# 参考资料

1、

https://meetonfriday.com/posts/736969d7/