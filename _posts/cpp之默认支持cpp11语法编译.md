---
title: cpp之默认支持cpp11语法编译
date: 2018-05-09 16:37:22
tags:
	- cpp

---



有两种方法，第一种是在cpp源代码里加入特殊注释。

写在第一行。

```
#pragma GCC diagnostic error "-std=c++11"
```

这种方式明显不太好。

第二种就是修改g++的别名。在~/.bashrc里加上。

```
alias g++='g++ -std=c++11'
```



# c++11

从名字上的11看，是2011年发布的标准。

现在c++17都出来了。

当前很多还是默认C++ 03的语法的。



# 参考资料

1、C++11常用特性的使用经验总结

https://www.cnblogs.com/feng-sc/p/5710724.html

2、C++14新特性总结 - C++98 -> C++03 -> C++11 -> C++14 -> C++17

https://blog.csdn.net/ztguang/article/details/53908407