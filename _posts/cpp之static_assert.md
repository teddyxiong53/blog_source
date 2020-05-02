---
title: cpp之static_assert
date: 2020-05-01 10:35:08
tags:
	- cpp

---

1

static_assert是一个关键字。

是C++0x开始引入的。

用来在编译时进行断言判断。所以也叫静态断言。

跟assert函数这个在运行时进行的动态断言相对应。

基本格式是：

```
static_assert(expr, "msg");
```

如果expr为false，那么就在编译时提示错误信息msg内容。

这样我们就可以在编译期间发现更多的隐藏问题。

强制保证一些约定被遵守。

帮助我们改进编译信息的可读性，尤其是在使用模板的时候。

static_assert的使用位置没有什么限制。

各种作用域里都可以用。

编译器在碰到一个static_assert的时候，通常情况是立刻把第一个参数作为常量表达式进行演算。

但是，如果该表达式依赖于某些模板参数，则会延迟到模板实例化的时候再进行演算。

这样就让检查模板参数变得可行了。

如何构造一个合适的常量表达式，是讨论的重点。



在性能方面，因为static_assert是在编译期间起作用，不会生成对应的目标代码，所以对运行性能是没有任何影响的。

看一个最简单的例子。

```
static_assert(sizoef(void*)==4, "64bit is not supported");
```

这个的作用就是提示用户，不支持64位系统。



参考资料

1、static_assert与assert

https://www.cnblogs.com/guxuanqing/p/10618816.html

