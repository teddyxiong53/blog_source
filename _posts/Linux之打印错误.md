---
title: Linux之打印错误
date: 2018-03-10 15:40:23
tags:
	- Linux

---



系统调用出错，怎么知道是什么原因导致的错误呢？

linux下常用2个函数strerror和perror来打印错误。

函数原型：

```
#include <string.h>
char *strerror(int errnum);
#include <stdio.h>
void perror(const char *msg);
```



另外还有一个全局变量errno。



我用来，觉得perror比较好用一点。

