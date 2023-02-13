---
title: cpp之STL
date: 2018-05-09 15:44:33
tags:
	- cpp
typora-root-url: ../
---



stl六大组件：

```
容器。
算法。本质是函数模板。
迭代器。连接容器和算法。
仿函数。普通函数指针可以看做最简单的仿函数。
适配器。stack、queue，看起来像是容器，但是实际是对deque的封装。
分配器。
```



stl的一个重要特点是数据结构和算法分离。

这个特点使得stl通用性非常好。

例如sort函数，你可以用来处理任何类型的数据。



stl的另外一个重要特性是基于模板，而不是面向对象。



容器

```
7种基本容器
vector
set
list
map
deque
multiset
multimap

看下面的图，容器可以分为两大类：
1、序列式容器。跟元素值无关，跟插入的时机有关。
2、关联式容器。跟插入时机无关，跟值有关系。
```

![](/images/cpp之容器图.png)

容器的选用原则：

```
1、需要频繁插入删除的，用list。
2、vector在头部操作效率低，在尾部操作效率高。
3、deque在头部和尾部操作效率高。
```



容器的遍历方法。

```
for(std::vector<int>::iterator it=xx.begin(); it!=xx.end(); it++) {
    
}
```



map和set的对比

```

```



关联式容器的内部结构是一棵平衡二叉树。这样搜索效率比较高。



迭代器

```
用来在一个对象集群里的元素进行遍历。
这个对象集群可以是容器，可以是容器的一部分。

迭代器的主要好处：
为所有容器提供了一组很小的公共接口。

每种容器都自己提供了迭代器。

```





# 参考资料

1、

https://blog.csdn.net/qq_31108501/article/details/55049937

2、三十分钟掌握STL 

http://net.pku.edu.cn/~yhf/UsingSTL.htm

3、C++之STL和Boost

https://blog.csdn.net/maweifei/article/details/70022691

