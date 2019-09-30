---
title: python之5个带key的内置函数
date: 2019-09-30 14:24:22
tags:		
	- python

---

1

max、min、filter、map、sorted。

```
In [6]: a = [1,2,3,-4]    

In [7]: max(a)            
Out[7]: 3

In [8]: max(a, key=abs)   
Out[8]: -4
```



filter用来过滤序列，返回一个迭代器对象。

```
2个参数
参数1：
	一个函数，可以为None。
参数2：
	序列。
```

```
In [15]: def is_odd(x): 
    ...:     return x%2==1 
    ...:                            

In [16]: filter(is_odd, a)          
Out[16]: <filter at 0x7fe31df4c9e8>

In [17]: print(list(_))             
[1, 3]
```



map是对序列进行映射的函数。

sorted是对序列进行排序的函数。



参考资料

1、python3 5个带key内置函数

https://www.cnblogs.com/jason-lv/p/8243141.html