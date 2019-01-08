---
title: python之defaultdict
date: 2019-01-03 13:40:59
tags:
	- python
---



defaultdict的default表示默认值，给dict里不存在的key，给一个default的value。

因为python默认对于不存在的key，是会抛出一个KeyError的异常的。

给默认值，需要一个类型（本质是工厂方法）。

有4种可能：int、set、list、str。

```
In [1]: from collections import defaultdict

In [2]: dict1 = defaultdict(int)

In [3]: dict2 = defaultdict(set)

In [4]: dict3 = defaultdict(list)

In [5]: dict4 = defaultdict(str)

In [6]: dict1['a']
Out[6]: 0

In [7]: dict2['a']
Out[7]: set()

In [8]: dict3['a']
Out[8]: []

In [9]: dict4['a']
Out[9]: ''
```



参考资料

http://kodango.com/understand-defaultdict-in-python



https://blog.csdn.net/dpengwang/article/details/79308064