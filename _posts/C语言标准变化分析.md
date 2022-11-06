---
title: C语言标准变化分析
date: 2018-10-11 11:36:51
tags:
	- 工具

---



C11之前的最新C标准是C99 。



要知道，任何一门编程语言都有相关的组织和团体在不停的维护和更新。

原因很简单，时代在发展，编程语言如果停滞不前，最终就会被淘汰。



以 C 语言为例，发展至今该编程语言已经迭代了诸多个版本，

例如 C89（偶尔又称为 C90）、C94（C89 的修订版）、C99、C11、C17，以及当下正在开发的 C2X 新标准。

甚至于在这些标准的基础上，GCC 编译器本身还对 C 语言的语法进行了扩展，

先后产生了 GNU90、GNU99、GNU11 以及 GNU17 这 4 个版本。



C++ 语言的发展也历经了很多个版本，包括 C++98、C++03（C++98 的修订版）、C++11（有时又称为 C++0x）、C++14、C++17，以及即将要发布的 C++20 新标准。和 C 语言类似，GCC 编译器本身也对不同的 C++ 标准做了相应的扩展，比如 GNU++98、GNU++11、GNU++14、GNU++17。



读者可能会问，这么多标准，GCC 编译器使用的到底是哪一套呢？

不同版本的 GCC 编译器，默认使用的标准版本也不尽相同。

以当前最新的 GCC 10.1.0 版本为例，默认情况下 GCC 编译器会以 GNU11 标准（C11 标准的扩展版）编译 C 语言程序，以 GNU++14 标准（C++14 标准的扩展版）编译 C++ 程序。





`bool` exists in the current C - C99, but not in C89/90.

In C99 the native type is actually called `_Bool`, while `bool` is a standard library macro defined in `stdbool.h` (which expectedly resolves to `_Bool`). Objects of type `_Bool` hold either 0 or 1, while `true` and `false` are also macros from `stdbool.h`.

Note, BTW, that this implies that C preprocessor will interpret `#if true` as `#if 0` unless `stdbool.h` is included. Meanwhile, C++ preprocessor is required to natively recognize `true` as a language literal.



# 参考资料

http://c.biancheng.net/view/8053.html