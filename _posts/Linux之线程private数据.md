---
title: Linux之线程private数据
date: 2019-07-30 17:55:19
tags:
	- Linux

---



线程局部存储，也叫TLS。

errno就是一个典型的tls。很好地解决了多线程下errno的值的正确性问题。

对于Linux下，只需要这样定义变量，就可以得到一个线程局部存储的变量。

```
static __thread int a;
```

上面说的是C语言层面的实现。

pthread也进行了实现。但是比较繁琐。

用pthread_key来表示这种变量。

就不深入看了。







参考资料

1、线程局部存储

https://zh.wikipedia.org/wiki/%E7%BA%BF%E7%A8%8B%E5%B1%80%E9%83%A8%E5%AD%98%E5%82%A8

2、linux编程 - C/C++每线程（thread-local）变量的使用

https://blog.csdn.net/jasonchen_gbd/article/details/51367650