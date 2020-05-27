---
title: cpp之demangle
date: 2020-05-27 22:17:08
tags:
	- cpp

---

1

看muduo代码里，有这样的变量名：

```
string stackTrace(bool demangle);
```

demangle具体是什么含义呢？

c++的代码在编译后，函数的名字会被编译器修改，改成编译器内部的名字。这个名字会在链接时被使用。

这个把源代码函数名字转换为c++ ABI标识符的过程，就叫做mangle。

反向的过程，则叫做demangle。



在C和C++的发展过程中，二进制兼容性一直是一个问题。

不同的编译器厂家编译的二进制代码之间的兼容性不好。甚至同一个编译器的不同版本之间的兼容性也不好。

后来，C有了统一的ABI。

而C++由于其本身的复杂性以及ABI标准推进不力，一直没有自己的ABI。



参考资料

1、mangle和demangle

https://www.cnblogs.com/BloodAndBone/p/7912179.html

2、C++ ABI 的稳定性：编程语言的发展

https://www.oracle.com/technetwork/cn/articles/servers-storage-dev/stablecplusplusabi-333927-zhs.html