---
title: Linux之signalfd
date: 2019-12-20 17:51:19
tags:
	- Linux
---

1

signalfd是用来创建一个fd，这个fd的作用是接收signal。

为什么要出现signalfd这种新东西？

signalfd实现了sigwaitinfo的功能。

但是它有一个好处，就是它的fd可以被select等io复用机制使用。

函数原型是这样：

```
#include <sys/signalfd.h>
int signalfd(int fd, const sigset_t *mask, int flags);
```

第一个参数有点费解，这个函数不是要产生一个fd吗？它的参数fd是干什么用的？

看man手册里：

```
If  the fd argument is -1, then the call creates a new file descriptor and associates the signal set specified in mask with that descriptor.  If fd is not -1, then it must spec‐
       ify a valid existing signalfd file descriptor, and mask is used to replace the signal set associated with that descriptor.
```

就一般参数fd都设置为-1就好了。



参考资料

1、man手册

2、linux新API---signalfd的使用方法

https://blog.csdn.net/yusiguyuan/article/details/22934743

