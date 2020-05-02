---
title: python之列表推导式
date: 2019-04-12 13:20:30
tags:
	- python

---

1

列表推导式，也叫列表生成式。

直接看例子。

```
In [1]: li = range(5)

In [2]: li
Out[2]: [0, 1, 2, 3, 4]

In [3]: print [x**2 for x in li]
[0, 1, 4, 9, 16]
```



还可以看复杂一点的一点。for循环加if，二层for循环的。

也都是常见的，实用的用法。

```
[ x * x for x in rang(5) if x%2==0 ]
```

```
[ m+n for m in 'abc' for n in 'xyz' ]
```

for循环里 if 后面不能跟else。因为if就是要进行筛选。



参考资料

1、Python的列表推导式

https://www.cnblogs.com/yupeng/p/3428556.html

2、Python的各种推导式（列表推导式、字典推导式、集合推导式）

https://blog.csdn.net/yjk13703623757/article/details/79490476

3、列表生成式

<https://www.liaoxuefeng.com/wiki/1016959663602400/1017317609699776>