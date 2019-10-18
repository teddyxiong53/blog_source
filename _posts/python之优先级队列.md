---
title: python之优先级队列
date: 2019-10-18 19:26:54
tags:
	- python

---

1

优先级队列，就是PriorityQueue。这种队列有什么具体用途？特点是什么？

底层使用堆来实现。

每次队首的优先级最高。

python3不允许插入优先级相同的值，或者无法判断优先级的值到优先队列。

插入的时候，加入一个index，就不会出现优先级相同的情况了。

在这个点上，python2和python3的表现是不一样的。

这个是因为python3在排序行为上发生了变化。

python3更加合理一些。对于不适合进行比较的对象，python2排的不对，python3直接抛出异常。



参考资料

1、priority_queue的常见用法

https://www.cnblogs.com/mengxiaoleng/p/11387601.html

2、Python 队列Queue和PriorityQueue

https://blog.csdn.net/weixin_42202547/article/details/85536548

3、python PriorityQueue

https://blog.csdn.net/OCR207208207208/article/details/88106109

4、玩转PriorityQueue

https://blog.csdn.net/yizhenn/article/details/52949436