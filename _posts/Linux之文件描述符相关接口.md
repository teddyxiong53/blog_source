---
title: Linux之文件描述符相关接口
date: 2019-03-20 11:53:32
tags:
	- Linux

---





这个文件，是看《Linux多线程服务器编程》这本书里的章节，觉得这个知识点很有启发，所以记录下来。

Linux新的创建文件描述符的syscall，都支持一个额外的flags参数。

可以指定O_NONBLCOK和FD_CLOEXEC。

例如这些接口：

```
accept4
eventfd2
inotify_init1
pipe2
signalfd4
timerfd_create
```

这些函数的最后的数字，表示参数的个数，区别于默认的函数。

例如accept4，是区别于默认accept函数只有3个参数。所以说明。



参考资料

1、Linux 新增系统调用的启示

https://blog.csdn.net/Solstice/article/details/5327881