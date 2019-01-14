---
title: python之enumerate
date: 2019-01-08 15:58:25
tags:
	- python

---



```
In [19]: Address = namedtuple("Address", "ip port")

In [20]: Address.ip = "192.168.0.1"                

In [21]: Address                                   
Out[21]: __main__.Address

In [22]: Address.ip                                
Out[22]: '192.168.0.1'
```

给Address指定了ip和port的成员。

但是Address实际上是一个元组。

这样就可以不用[0]这样来获取内存，而可以直接用成员名字。

参考资料

1、

https://blog.csdn.net/zV3e189oS5c0tSknrBCL/article/details/78496429

