---
title: python之列表推导式
date: 2019-04-12 13:20:30
tags:
	- python

---



直接看例子。

```
In [1]: li = range(5)

In [2]: li
Out[2]: [0, 1, 2, 3, 4]

In [3]: print [x**2 for x in li]
[0, 1, 4, 9, 16]
```



tuple、list、dict，这3种类型，都有对应的推导式。



参考资料

1、Python的列表推导式

https://www.cnblogs.com/yupeng/p/3428556.html

2、Python的各种推导式（列表推导式、字典推导式、集合推导式）

https://blog.csdn.net/yjk13703623757/article/details/79490476