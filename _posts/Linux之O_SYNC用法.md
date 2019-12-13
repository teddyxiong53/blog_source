---
title: Linux之O_SYNC用法
date: 2019-12-12 13:40:38
tags:
	- Linux

---

1

O_SYNC是open函数的一个flag，我之前没有用到过。现在看/dev/mem进行mmap的时候，设置了这标志。

了解一下。

另外，还有一个O_DIRECT，跟这个关系比较紧密，一起看看。

O_DIRECT：无缓冲地进行输入和输出。

O_SYNC：以同步的方式打开文件。



# O_DIRECT

这个运行应用程序在执行磁盘io的时候，绕过高速缓存，直接把数据传递到磁盘。

这个就叫直接IO。也叫raw IO。

这个是给数据库程序用的。

可能会存在数据不一致的情况。

```
2个进程同时打开同一个文件。
进程A以O_DIRECT方式打开。
进程B以普通方式打开。
这样高速缓存里的和磁盘上的内容就可能出现不一致的情况。
需要注意避免这种情况出现。
```

# O_SYNC

这个叫同步IO。

同步io的定义是：

某一个io操作，要么成功，要么不成功。

有fsync、sync、fdatasync这几个函数可以用。





参考资料

1、O_DIRECT与O_SYNC区别

https://www.cnblogs.com/zl1991/p/10288291.html