---
title: Python之常用内置方法
date: 2017-09-30 23:19:37
tags:
	- Python

---



Python提供了一些基本的函数，下面把常用的列出来。

从Python2.7的帮助文档里梳理出来的。

# abs(x)函数

x可以是int、float、复数。返回绝对值。

# all(iterable)函数

看元素是不是都是真，如果是，返回True。

```
>>> a = (1,2)
>>> all(a)
True
>>> a = (0,1)
>>> all(a)
False
```

# any(iterable)函数

和all对应，这个是只要一个位真，就返回True。

# basestring类

是str和unicode类的父类。不能直接用，一般是用来判断字符串。

```
>>> a = "xxx"
>>> isinstance(a, basestring)
True
>>> a = (1,2)
>>> isinstance(a, basestring)
False
```

# bin(x)方法

这个就是返回一个int值对应的二进制字符串。

```
>>> bin(16)
'0b10000'
```

# callable(object)

看例子就懂了。

```
>>> a = (1,2)
>>> callable(a)
False
>>> a = lambda x:x+1
>>> callable(a)
True
```

# chr(i)

传递进来的参数是一个int类型。从这个函数的形参的写法，就可以看出Python的形参的规律。

x：不限定。

i：整数。

iterable：

object：

```
>>> chr(90)
'Z'
```



# classmethod

不知道有什么实际用途。

# cmp(x,y)函数

```
>>> cmp(1,2)
-1
>>> cmp(1,1)
0
>>> cmp(2,1)
1
```

# delattr(object, name)

删除属性。

# dict([arg])



# dir([object])



# eval(expression, globals, locals)



# float类

```
>>> float(2)
2.0
```

# 

# max/min函数

```
max([1,2,3])
max(1,2,3)

>>> d = {"a":1,"b":2,"c":3}
>>> max(d)
'c'
```

# sum函数

```
>>> sum([1,2,3],100)
106
>>> sum([1,2,3])
6
```

# sorted函数

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





