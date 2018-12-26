---
title: clang（一）
date: 2018-04-13 15:55:19
tags:
	- clang

---



经常看到clang这个东西，不知道是个啥，现在简单了解一下。

# 什么是clang？

clang是一个轻量级的编译器，可以编译c、c++。

基于bsd协议开源。

说到开源编译器，首先想到的就是gcc，有了这么强大的gcc，clang存在意义是什么呢？

也就是说，它有哪些特别的地方，是gcc不具备的。

1、较快的编译速度，较少的内存占用。这个对于一个编译器并不是关键。

2、兼容了gcc。

3、最大的优势就是license。



# clang和llvm的关系

llvm是一个框架，用来做编译器的框架。是用c++写的。

主要是苹果公司在支持。

开始于2000年。

clang相当于编译器的前段，llvm相当于编译器的后端。

所以说“XCode用的编译器是应该是LLVM”是不对的。XCode用的编译器是Clang。Clang是一个基于LLVM开发的C/C++/Obj-C编译器，有一套独立的前端，后端直接采用LLVM。

LLVM是Apple官方支持的编译器，而该编译器的前端是Clang，这两个工具都被集成到了Xcode里面。

很长一段时间，Apple都是用gcc作为官方的编译器的。

但是gcc对于Apple的很多object-c语言的新特性不及时支持，所以Apple也一直在寻找替代方案。

最后选中了llvm。

llvm的作者现在就在Apple工作。该作者也是Swift语言的主导设计者。Chris Lattern是苹果开发者工具部门的主管。领导者Xcode和编译器团队。





# 安装使用

本来不打算用的。

但是学习uwebsocket这个的时候，发现这个居然是clang编译的。

那就安装吧。

```
 sudo apt-get install clang
```



# 参考资料

1、clang

https://baike.baidu.com/item/clang/3698345?fr=aladdin

2、Clang 比 GCC 好在哪里？

https://www.zhihu.com/question/20235742

3、LLVM与Clang的概述及关系

https://blog.csdn.net/talentedlas/article/details/51945569

4、LLVM和Clang背后的故事

https://blog.csdn.net/zhouzhaoxiong1227/article/details/52166942