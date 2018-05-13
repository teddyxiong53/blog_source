---
title: cpp之std疑问
date: 2018-05-13 21:04:40
tags:
	- cpp

---



这篇文章就逐渐把碰到的std的内容整理起来。



# pair

https://www.cnblogs.com/lvchaoshun/p/7769003.html

pair是把2个数据组合成一个数据。

pair实质上是一个结构体。

两个成员变量是first和second。

产生一个pair，有两种方法：

1、用构造函数。

2、用make_pair函数。

```
std::pair<int, float>(1, 1.1);
std::make_pair(1, 1.1);
```

需要包含头文件。

```
#include <utility>
```



