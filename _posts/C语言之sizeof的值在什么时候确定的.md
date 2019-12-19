---
title: C语言之sizeof的值在什么时候确定的
date: 2019-12-18 15:34:22
tags:
	- C语言

---

1

在K&R的书里，写的是sizeof是在编译时确定值的。

但是从C99开始，引入了动态数组。

```
printf("sizeof 'a' is:%d\n", sizeof('a'));
```

上面这一行代码，

在C语言里，打印出来是4，而在C++里，打印出来是1 。

C中sizeof侧重于“数”，而C++中sizeof更侧重于“字符”。

```
//适用于非数组
#define _sizeof(T) ((size_t)((T*)0 + 1))
//适用于数组
#define array_sizeof(T) ((size_t)(&T+1)-(size_t)(&T))
```



参考资料

1、C语言中 sizeof 运算的值是在编译时还是运行时确定？

https://blog.csdn.net/keykey__7/article/details/53334922

