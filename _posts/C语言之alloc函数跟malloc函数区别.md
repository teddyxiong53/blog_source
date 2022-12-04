---
title: C语言之alloc函数跟malloc函数区别
date: 2022-12-02 21:03:25
tags:
	- C语言

---

--

看libev的代码，有这样的语句：

```
ev_realloc (void *ptr, long size)
{
  ptr = alloc (ptr, size);

```

alloc这个函数，跟malloc函数有什么区别呢？



alloc 的调用序列与 malloc 相同,

与 malloc 不同的是

alloc 在当前的函数的栈帧上分配存储空间,而不是在堆中.（**那就是跟alloca类似了**）

这样做的好处是:

函数返回时,自动释放它所使用的栈帧,所以不必再为释放空间而费心.

也就是说不必要担心操作它的释放问题.

同样这样处理的其缺点也很明显:

某些系统在函数已被调用后不能增加栈帧长度,于是也就不能支持 alloc 函数.

**尽管如此,很多软件包还是使用 alloc 函数,也有很多系统支持它.**





参考资料

1、

http://www.yanceymichael.com/2018/03/07/%E5%AF%B9%E4%BA%8Emalloc%E3%80%81alloc%E3%80%81calloc%E3%80%81realloc%E7%9A%84%E5%8C%BA%E5%88%AB%E6%B5%85%E6%98%BE%E7%9A%84%E7%90%86%E8%A7%A3/