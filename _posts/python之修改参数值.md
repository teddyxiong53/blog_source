---
title: python之修改参数值
date: 2019-01-09 13:47:22
tags:		
	- python

---



在C和c++里，如果要修改参数的值，需要传递指针给函数。

那么在Python里，是怎样处理的呢？



```
In [64]: a = 'c'

In [65]: type(a)
Out[65]: str

In [66]: def func(x):
   ....:     x = 'a'
   ....:     

In [67]: func(a)

In [68]: print a
c

In [69]: a = ['a', 'b']

In [70]: def func2(l):
   ....:     l[0] = 'x'
   ....:     

In [71]: func2(a)

In [72]: print a
['x', 'b']
```

普通变量，修改不了。

list这种，可以修改。



参考资料

1、Python的函数参数传递：传值？引用？

http://winterttr.me/2015/10/24/python-passing-arguments-as-value-or-reference/