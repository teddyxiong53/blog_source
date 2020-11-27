---
title: python之pandas
date: 2020-11-23 11:01:30
tags:
	- python
---

1

Pandas是用于数据操纵和分析，建立在Numpy之上的。

Pandas为Python带来了两种新的数据结构：

Pandas Series和Pandas DataFrame，

借助这两种数据结构，我们能够轻松直观地处理**带标签数据**和关系数据。

Pandas功能：

- 允许为行和列**设定标签**
- 可以针对时间序列数据计算滚动统计学指标
- 轻松处理NaN值
- 能够将不同的数据集合并在一起
- 与Numpy和Matplotlib集成

Pandas series 是像数组一样的一维对象，可以存储很多类型的数据。

Pandas series 和 Numpy array之间的主要区别之一是

你可以为Pandas series 中的每个元素分配索引标签；

另一个区别是Pandas series 可以同时存储不同类型的数据。

```
import pandas as pd

groceries = pd.Series(
    data=[30, 6, 'yes', 'no'],
    index=['eggs', 'apples', 'milk', 'bread']
)

print(groceries.size)
print(groceries.shape)
print(groceries.ndim)
print(groceries.index)
print(groceries.values)
```

得到：

```
4
(4,)
1
Index(['eggs', 'apples', 'milk', 'bread'], dtype='object')
[30 6 'yes' 'no']
```

查看某个标签是否在序列里。

```
print('book' in groceries)
```

访问序列的切片和索引

Pandas Series 提供了两个属性 .loc 和 .iloc

.loc 表明我们使用的是标签索引访问

.iloc 表明我们使用的是数字索引访问

标签索引

```
print(groceries['eggs'])
print(groceries[['eggs', 'milk']])
```

得到：

```
30
eggs     30
milk    yes
dtype: object
```

数字索引

```
print(groceries[1])
print(groceries[[1,2]])
print(groceries[-1])
```

得到：

```
6
apples      6
milk      yes
dtype: object
no
```



pandas的切片功能非常强大，使用恰当的话可以大大提升工作效率



参考资料

1、Python常用库之二：Pandas

https://www.cnblogs.com/feifeifeisir/p/10495976.html

2、

https://blog.csdn.net/zhangcongyi420/article/details/103909107