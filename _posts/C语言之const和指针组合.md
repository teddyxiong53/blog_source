---
title: C语言之const和指针组合
date: 2019-12-16 09:40:22
tags:
	- C语言

---

1

首先看const修饰普通变量的情况。

```
const int a = 1;//推荐用这种。
int const a = 1;
//这2个是等价的。
```

const跟指针的搭配：

```
const int *p1; //const限制的是是*p1，p1可以被赋值为其他指针，传参时经常用。算是最常见的用法。
int const *p2;//跟第一种是一样的，int和const位置换了不影响，关键是*的位置。
int * const p3;//这个就跟p1不同了。限制的是p3，而不是*p3，就是p3不能再改成指向其他指针，但是*p3可以被修改。
```



参考资料

1、c语言中const关键字的作用，以及const同指针的常见组合方式

https://blog.csdn.net/Andy1814/article/details/87943834