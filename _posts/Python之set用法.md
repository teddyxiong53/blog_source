---
title: Python之set用法
date: 2018-11-26 21:34:23
tags:
	- Python

---



set这种数据类型用得比较少。但是还是要把用法学习一下。

frozenset内容不能修改。

set意思是集合。里面不能包含重复元素。

接收一个list作为参数。

```
list1 = [1, 2, 3]
s1 = set(list1)
print s1
```

增加元素。

add函数。

删除元素。

remove函数。

求2个set的交集和并集。

```

In [14]: list1 = [1, 2, 3]

In [15]: s1 = set(list1)

In [16]: print s1
set([1, 2, 3])

In [17]: s2 = set([2,3,4])

In [18]: print s1&s2
set([2, 3])

In [19]: print s1|s2
set([1, 2, 3, 4])
```

大中小括号都可以，但是不能没有。

```
In [23]: s2 = frozenset(("c","d"))

In [24]: s2
Out[24]: frozenset({'c', 'd'})

In [25]: s2 = frozenset({"c","d"})

In [26]: s2
Out[26]: frozenset({'c', 'd'})

In [27]: s2 = frozenset(["c","d"])

In [28]: s2
Out[28]: frozenset({'c', 'd'})
```



# 参考资料

1、python中set()函数的用法

https://blog.csdn.net/csdn15698845876/article/details/78244491

2、python中set和frozenset方法和区别

https://www.cnblogs.com/panwenbin-logs/p/5519617.html