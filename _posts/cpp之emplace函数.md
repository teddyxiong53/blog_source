---
title: cpp之emplace函数
date: 2019-04-10 17:28:31
tags:
	- cpp

---



1

c++11里，往容器里添加元素，除了之前是insert、push_back这些函数外，新增了emplace函数。

emplace的字面意思是放置。

例如你往一个vector的后面添加一个元素。

```
vector<int> nums;
nums.push_back(1);

也可以这样
nums.emplace_back(1);
```

这二者的区别是什么呢？

emplace最大的作用就是避免临时变量的产生。

因为它可以完成in place的构造。

这个是依靠c++11的2个新特性来做到的。

```
1、变参模板。
2、完美转发。
```



map的emplace函数有些特殊。

emplace的提升也没有想象的那么大。



参考资料

1、C++11 中的 emplace

http://blog.guorongfei.com/2016/03/16/cppx-stdlib-empalce/

2、c++11 之emplace_back 与 push_back的区别

https://blog.csdn.net/p942005405/article/details/84764104