---
title: java之常用基础数据结构
date: 2017-12-20 20:33:05
tags:
	- java
typora-root-url: ..\
---



我们先重点看集合类型的。这些都是在java.util包下面的。

总的来说，分为两类：Collection和Map。这是2个接口。

先看总体的集合框架体系图。

![java集合框架体系图](/images/java集合框架体系图.png "java集合框架体系图")

Iterator接口是所有集合的共同接口。是用来遍历所有元素的。主要包含hasNext、next、remove这3个接口。

# Collection

##子类

1、List。

2、Set。

3、Queue。

4、SortedSet。

## 函数

增：

```
add()
addAll()
```

删：

```
remove
removeAll
removeIf
```

改：

```
toArray：集合变数组
```

查：

```
isEmpty
contains
size()
containsAll
equals
```

# List 

ArrayList是线程不安全的。Vecotr是线程安全的，但是效率低。

# Set

所有的Set子类都是线程不安全的。

鉴于在开发中经常会碰到区分同一个对象的问题，一个完整的类应该覆盖Object的hashCode、equals、toString这3个方法。

# Collections

这个是一个工具类的名字。里面定义都是静态方法。





