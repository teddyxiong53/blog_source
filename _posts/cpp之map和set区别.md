---
title: cpp之map和set区别
date: 2020-06-04 09:44:08
tags:
	- cpp

---

1

最基本的区别：

map里放的是一个key-value对。

而set放的元素只有key。没有value。

如果set里要放一个键值对。先用pair包装一下。

```
typedef std::pair<Timer*, int64_t> ActiveTimer;
typedef std::set<ActiveTimer> ActiveTimerSet;
```



set和map的底层实现都是红黑树。



set和map的所有区别：

```
1、set只有key。map有key-value对。
2、set的迭代器是const的。所以不能修改set里的内容。
	map的迭代器可以修改value，不能修改key。
	因为set和map都是依赖key来保证它们的有序性的。
3、map支持下标操作，set不支持下标操作。
```





参考资料

1、map和set有什么区别，分别又是怎么实现的？

https://blog.csdn.net/qq_41007781/article/details/93627188