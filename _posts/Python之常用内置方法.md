---
title: Python之常用内置方法
date: 2017-09-30 23:19:37
tags:
	- Python

---



Python提供了一些基本的函数，下面把常用的列出来。

# 1. max/min函数

```
max([1,2,3])
max(1,2,3)

>>> d = {"a":1,"b":2,"c":3}
>>> max(d)
'c'
```

# 2. sum函数

```
>>> sum([1,2,3],100)
106
>>> sum([1,2,3])
6
```

# 3. float类

```
>>> float(2)
2.0
```

# 4. sorted函数

函数原型是这样：

```
sorted(...)
    sorted(iterable, cmp=None, key=None, reverse=False) --> new sorted list
```

```
>>> sorted("bca")
['a', 'b', 'c']
>>> sorted([3,1,2])
[1, 2, 3]
```





