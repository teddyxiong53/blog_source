---
title: linux之timerfd使用
date: 2019-02-23 17:11:17
tags:
	- Linux

---



是Linux为用户态程序提供的接口。基于文件描述符进行操作。

主要用于select和poll。

我在看muduo的代码里看到这个东西。所以了解一下。

主要有3个接口。

```
timerfd_create
timerfd_settime
timerfd_gettime
```

举例：

```

```



参考资料

1、linux新定时器：timefd及相关操作函数

https://www.cnblogs.com/mickole/p/3261879.html

