---
title: Linux内核之copy_to_user分析
date: 2019-12-11 13:34:38
tags:
	- Linux

---



在驱动里，应用层跟内核交互数据，有copy_to_user这一系列的函数。

看看copy_to_user的实现。

如果没有MMU，copy_to_user其实就是memcpy的一个宏。

```
#define __copy_to_user(to,from,n)	(memcpy((void __force *)to, from, n), 0)
```

有mmu，最后也是memcpy的。

同类型的函数还有put_user、get_user。



copy_to_user在每次拷贝的时候，都需要检查指针的合法性。

检查的内容是：用户空间的指针所指向的地址确实是属于该进程本身的，而不是指向了不属于它的地方。



因为虚拟地址连续，物理地址不一定连续（而且是往往不连续），造成了cpu cache频繁失效，使得访问速度降低。



mmap只在第一次访问的时候为进程建立页表，之后不再检查地址的合法性。

mmap一般是把一段连续的物理地址映射成一个虚拟地址，这样效率会高很多。



在内核空间和用户空间交换数据时，

get_user和put_user是两个两用的函数。

相对于copy_to_user和copy_from_user(将在另一篇博客中分析)，

这两个函数主要用于完成一些简单类型变量(char、int、long等)的拷贝任务，

对于一些复合类型的变量，比如数据结构或者数组类型，

get_user和put_user函数还是无法胜任，

这两个函数内部将对指针指向的对象长度进行检查，

在arm平台上只支持长度为1，2，4，8的变量。

下面我具体分析，首先看get_user的定义(linux/include/asm-arm/uaccess.h)：


# 参考资料

1、copy_to_user与mmap的工作原理

https://blog.csdn.net/do2jiang/article/details/5403802

2、linux内核中的get_user和put_user

https://blog.csdn.net/ce123_zhouwei/article/details/8457822