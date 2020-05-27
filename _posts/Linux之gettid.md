---
title: Linux之gettid
date: 2020-05-27 22:50:08
tags:
	- Linux

---

1

获取线程的id，gettid。

可能有的情况会报这个函数找不到的错误。

可以自己使用系统调用来做。

```
#define __NR_gettid     224
```

```
#include <sys/syscall.h>
printf("The ID of this thread is: %ld\n", (long int)syscall(224));
```



更好的方式是：

```
#include <sys/syscall.h>
#define gettidv1() syscall(__NR_gettid)
#define gettidv2() syscall(SYS_gettid)
printf("The ID of this thread is: %ld\n", (long int)gettidv1());// 最新的方式
printf("The ID of this thread is: %ld\n", (long int)gettidv2());// traditional form
```



参考资料

1、Linux下获取线程TID的方法——gettid()

https://blog.csdn.net/delphiwcdj/article/details/8476547