---
title: Python之iterable
date: 2017-09-30 23:23:06
tags:
	- Python

---



可直接用作for循环的数据类型有：

1、集合类的。如list、tuple、dict、set、str等。

2、生成器。例如带yield的函数。

这些可以直接用作for循环的对象统一叫做可迭代对象。Iterable。

可以用instance()函数来判断是否是Iterable对象。

```
>>> isinstance([], Iterable)
True
>>> isinstance({}, Iterable)
True
>>> isinstance(100, Iterable)
False
```

除了可以用在for循环，还可以使用next来遍历的，叫做迭代器。Iterator。

也可以用isinstance来判断。

```
>>> isinstance([], Iterator)
False
>>> isinstance((x for x in range(10)), Iterator)
True
```

tuple、list、dict都不是Iterator。为什么？

因为Python里的Iterator表示的是一个数据流。我们可以理解为一个有序序列，但是不能提前知道它的长度。只有通过next函数才能获得下一个。它是惰性的。

Iterator可以用来表示一个无限大的数据流，例如全体自然数。而这个是普通的list这些做不到的。



