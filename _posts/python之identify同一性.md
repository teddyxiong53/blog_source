---
title: python之identify同一性
date: 2020-11-06 17:36:30
tags:
	- python
---

1

看python代码里，有identify这个函数，定义是这样：

```
_identity = lambda x: x
```

这个的意义是什么？

identify的含义是同一性？

什么是同一性？

在数学上，一个同一性函数，就是f(x)=x.

表示函数的值跟参数是一样的。



is是python的同一性运算符。

is和==两种运算符在应用上的本质区别是什么。



在讲is和==这两种运算符区别之前，首先要知道**Python中对象包含的三个基本要素**，分别是：

id(身份标识)、[python type()](http://www.iplaypy.com/jichu/type.html)(数据类型)和value(值)。

is和==都是对对象进行比较判断作用的，但对对象比较判断的内容并不相同。

下面来看看具体区别在哪。

```
a=10
b=10
print(a == b)
print(a is b)
```

这2个都是True。

is也被叫做同一性运算符，这个运算符比较判断的是对象间的唯一身份标识，也就是id是否相同。



==比较操作符：用来比较两个对象是否相等，value做为判断因素；
is同一性运算符：比较判断两个对象是否相同，id做为判断因素。



参考资料

1、

https://en.wikipedia.org/wiki/Identity_function

2、Python is同一性运算符和==相等运算符区别

https://blog.csdn.net/lemontree1945/article/details/78810658