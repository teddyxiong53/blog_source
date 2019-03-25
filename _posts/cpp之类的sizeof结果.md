---
title: cpp之类的sizeof结果
date: 2019-03-25 17:10:32
tags:
	- cpp

---



看muduo的代码，有这样的静态断言。

```
static_assert(sizeof(Timestamp) == sizeof(int64_t),
              "Timestamp is same size as int64_t");
```

但是Timestamp是一个class。里面成员变量虽然是只有一个int64，但是还有一堆的函数啊。

为什么它的sizeof是跟成员变量的大小一样呢？



一个空类也要实例化。

你用sizeof来看一个空类的大小，会得到是1一个字节。一个类的实例对应内存上的一个地址。

编译器会默认给空类加上一个字节。

函数因为是只读的，所以一个类的多个实例是共用一个地址的。所以函数不能算到sizeof里去。



参考资料

1、类的大小——sizeof 的研究(1)

https://blog.csdn.net/hairetz/article/details/4171769