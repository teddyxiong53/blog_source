---
title: cpp之算法库
date: 2018-09-08 17:22:35
tags:
	- cpp

---



算法库提供大量的函数，用来完成查找、排序等功能。

他们在元素范围上操作，范围定义为`[first, last)`。

相当于

```
for(i=first; i<last; i++)
```



大多数算法拥有接受执行策略的重载。

标准算法库提供3种执行策略：有序、并行和并行加向量。



大多数都定义在头文件algorithm里。



# 参考资料

1、算法库

https://zh.cppreference.com/w/cpp/algorithm