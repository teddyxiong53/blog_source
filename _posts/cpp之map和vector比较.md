---
title: cpp之map和vector比较
date: 2020-05-26 14:39:08
tags:
	- cpp

---

1

首先，不管是vector还是map，请尽量存取指针，否则在存取时会有数据拷贝带来不必要的时间损失。通常用int和string做key的场景比较普遍（我的项目即如此），能用int作key就用int作key，效率比string高。



vector和set的比较

vector相比于其他的容器，有一个很大的特点，就是它是顺序存储的。

这个带来了可以下标访问，随机访问的好处。带来了插入效率低的坏处。

**vector：擅长于解决某个位置是什么值的问题。**

**set：擅长于解决某个元素在哪个位置的问题。**



参考资料

1、vector和map的效率简要比较

https://blog.csdn.net/bodybo/article/details/75220126

2、vector,map以及list性能对比

https://blog.csdn.net/Think88666/article/details/89318449

3、vector和set的区别

https://blog.csdn.net/stone_flower_rain/article/details/82771820