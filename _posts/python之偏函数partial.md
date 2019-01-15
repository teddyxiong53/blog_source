---
title: python之偏函数partial
date: 2019-01-15 15:54:59
tags:
	- python
---



就是可以先把函数的一部分参数传递过去。

然后再传递另外一部分。

```
In [17]: from functools import partial

In [18]: def add(a,b):
   ....:     return a+b
   ....: 

In [19]: add(4,3)
Out[19]: 7

In [20]: plus=partial(add, 100)

In [21]: plus(20)
Out[21]: 120
```

主要是用来对函数进行重新定义，方便使用。在频繁使用的时候，减少多次写同一个参数。





参考资料

1、python中的偏函数partial

https://www.cnblogs.com/zhaopanpan/p/9397485.html