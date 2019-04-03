---
title: java之反射
date: 2019-04-03 13:21:04
tags:
	- java

---



java为什么可以反射？

反射依赖编译器为class生成的元信息。

运行时类型识别（RTTI）。

靠的就是编译时，对每一个定义的java类，都有一个对应的Class对象。



反射最重要的用途就是开发各种通用框架。



参考资料

1、Java为什么要有反射机制，而 C++ 没有？

https://www.zhihu.com/question/42098040

2、深入理解Java类型信息(Class对象)与反射机制

https://blog.csdn.net/javazejian/article/details/70768369

3、说说反射的用途及实现

https://www.jianshu.com/p/d6035d5d4d12