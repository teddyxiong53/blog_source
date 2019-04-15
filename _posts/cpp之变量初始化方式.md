---
title: cpp之变量初始化方式
date: 2018-10-13 11:13:51
tags:
	- cpp
---



cpp的初始化有两种：

1、等于的方式。

2、小括号方式。

```
第一种情况： XX aa = a;
第二种情况： XX aa(a);
第三种情况： extern fun(XX aa); fun(a)函数调用
第四种情况： XX fun(){...}; XX a = fun();函数返回值的时候
```



c++11统一了。

````
无论是类的变量，数组，stl的容器，类的构造，都统一使用{}。
````



参考资料

1、c++类对象初始化方式总结

https://blog.csdn.net/caoyan_12727/article/details/52469065

2、C++11列表初始化

https://blog.csdn.net/K346K346/article/details/55194246

3、C++ 11 新特性之统一初始化语法

https://blog.csdn.net/wocacaaa/article/details/25784861