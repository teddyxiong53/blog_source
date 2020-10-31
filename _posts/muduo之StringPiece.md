---
title: muduo之StringPiece
date: 2020-06-01 10:32:08
tags:
	- muduo

---

1

为什么要单独一个StringPiece类呢？

C++自带的std::string不能满足要求吗？

这个类是从谷歌的代码里提取出来的，从注释里可以看到。

头部的注释这样写着：

```
// Author: Sanjay Ghemawat
//
// A string like object that points into another piece of memory.
// Useful for providing an interface that allows clients to easily
// pass in either a "const char*" or a "string".
//
// Arghh!  I wish C++ literals were automatically of type "string".
```

一个看起来像string的对象，它指向的是其他地方的内存。

允许使用者传递一个`const char *`或者`string`类型的参数。



**这个类实际上只是对字符串的一个Proxy类，使用的是设计模式里的代理模式。**

一般被称为string view。

它提供了一个窗口，外部只能观察到这个窗口里的内容。

在调整窗口的时候，不需要修改原字符串。

只需要移动开始指针和调整长度就可以了。

**另外，这个类本身不存储这个字符串。**

**所以，它的生存有效期取决于源字符串的生命周期。**





C++里有string和char *可以用来表示字符串。

如果你使用const string&来函数形参，就可以同时兼容string和char*。

但是，当你传入一个很长的char *的时候，会生成一个较大的string对象，这个开销比较大。

如果你的目的，仅仅是读取字符串的值，使用StringPiece的开销，则只是一个指针的开销。

同时也保证了兼容性。



参考资料

1、muduo::StringPiece？

https://www.zhihu.com/question/34499426/answer/58891014

2、

https://blog.csdn.net/q5707802/article/details/78420629