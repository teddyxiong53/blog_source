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



# qt和stl对比

QTL比起STL的话，**最大的特点是统一用了写时复制技术。缺点是不支持用户自定allocator。**

在这里先简单类比下吧，具体数据可以看后面的benchmark

- **QLinkedList —— std::list** 两者都是双向链表，两者可以直接互转。
- **QVector —— std::vector** 两者都是动态数组，都是根据sizeof(T)进行连续分配，保证成员内存连续，能够用data()直接取出指针作为c数组使用，两者可以直接互转。
- **QMap —— std::map** 两者都是红黑树算法，但不能互转，因为数据成员实现方式不同。std::map的数据成员用的是std::pair，而QMap用的是自己封装的Node，当然还是键值对.
- **QMultiMap —— std::multimap** 同上。
- **QList —— 暂无**。QList其实不是链表，是优化过的vector，官方的形容是array list。它的存储方式是分配连续的node，每个node的数据成员不大于一个指针大小，所以对于int、char等基础类型，它是直接存储，对于Class、Struct等类型，它是存储对象指针。

`QList还规避了模板最大的问题——代码量膨胀。由于QList其实是用void*存储对象，所以它的绝大部分代码是封装在了操作void*的cpp里，头文件只暴露了对其的封装。`



- **可靠性**——二者都有长期在大型系统级商业应用上使用的经历，并且除了c++11版本特性引入外，代码实现上基本没有大的变动，所以可靠性均无问题。当然，**为了保证效率，两者都不提供thread safe**，最多提供reentrant
- **安全性**——Qt变量存STL不存在安全隐患，毕竟都是class，只要是支持copy constructor和assignment operator的对象，都可以放心存STL。而且由于Qt对象广泛使用了写时复制机制，所以存储时时空开销非常小。



## 总结 

　　QTL比起STL，性能差别不明显，主要差异在：

1. QTL不支持allocator；
2. QTL没有shirnk接口（最新的几个版本里有了，不过不叫shirnk）；
3. QTL没有rbegin()/rend()（同上，最近几个版本有了，相同API名称）;
4. QTL对c++11特性的支持较晚（同上，Qt5.6开始才全面支持新特性），在这之前的版本，比起支持比如右值引用的STL版本，性能要略差。



参考资料

1、

https://zhuanlan.zhihu.com/p/24035468

# 参考资料

1、

https://blog.csdn.net/qq_31108501/article/details/55049937

2、三十分钟掌握STL 

http://net.pku.edu.cn/~yhf/UsingSTL.htm

3、C++之STL和Boost

https://blog.csdn.net/maweifei/article/details/70022691

