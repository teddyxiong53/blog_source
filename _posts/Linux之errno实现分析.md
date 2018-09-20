---
title: Linux之errno实现分析
date: 2017-10-02 13:58:17
tags:
	- Linux

---



Linux的errno，实际上不是一个我们通常认为的整型值，而是通过整型指针来取值的。这样可以做到线程安全。（？？）

```
extern int *__errno_location();
#define errno (*__errno_location ())
```

Linux里系统调用的错误都存放在errno里。

errno由os维护。下一次的错误会覆盖上一次的。

只有系统调用出错时，才会修改errno。

为什么会需要errno？这是一个无奈之举。

更多地算是一个技巧。而不是架构上的需要。

因为有些函数返回的是指针，这样就没法根据返回值来判断错误。

于是就借助errno来存储错误信息。



在gcc里，是通过把errno设置为线程局部变量来解决多线程的问题的。



其实，通过gcc编译一般的应用程序时__LIBC都是没有定义的。



# 参考资料

1、errno（包含一些不成熟的分析）

http://blog.chinaunix.net/uid-20753106-id-3944921.html

2、Linux errno详解

https://www.cnblogs.com/Jimmy1988/p/7485133.html

3、errno多线程安全

http://www.cnblogs.com/shijingxiang/articles/5234871.html

4、linux中的errno，你是否踩过它的坑？

https://blog.csdn.net/scaleqiao/article/details/46056349