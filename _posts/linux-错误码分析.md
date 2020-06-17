---
title: linux 错误码分析
date: 2016-11-04 21:05:40
tags:
	- linux
---


linux的错误码主要分布在这几个文件里。以arm架构的为例。源代码是linux2.6.35.7。

```
./include/asm-generic/errno-base.h -- 定义了1到34号错误。是最基础的一个文件。
./include/asm-generic/errno.h --包含了errno-base.h，并定义了35到132号错误。
./arch/arm/include/asm/errno.h -- 这个就是包含了./include/asm-generic/errno.h，没别的内容。
./include/linux/errno.h --包含了./arch/arm/include/asm/errno.h，并且定义了512到530号错误。
```

内核里，错误一般都是加上一个负号，为什么这么做？

例如这样：

```
error = button->gpio;
if (error != -ENOENT) {
if (error != -EPROBE_DEFER)
dev_err(dev,
"Failed to get gpio flags, error: %d\n",
error);
return ERR_PTR(error);
}
```

内核中的函数通常**以返回指针的形式来传递调用函数后执行的结果**，返回值指针有三种结果：
（1）调用成功则返回一个有效指针
（2）调用失败返回NULL，例如malloc、kmalloc、vmalloc
（3）**调用失败返回错误信息指针（无效指针）**
我们就是通过这个错误指针来传递有关错误的信息。



在linux中虚拟内存空间的分配，0-3G是给用户空间的，而3G-4G是给linux内核的，而0xFFFFF000就位于linux内核的虚拟内存空间范围内，内核返回的指针（ptr）通常指向页的边界（4KB），ptr指向的空间不会在（0xFFFFF000~0xFFFFFFFF）区间（因为小于一页），即：ptr & 0XFFF == 0；而一般内核出错代码返回值是一个负数，在 -1000~0之间，转变成unsigned long型，刚好在（0xFFFFF000~0xFFFFFFFF）区间。**所以就可以用(unsigned long)ptr > (unsigned long)-1000L来判断内核函数的返回值是一个有效的指针，还是一个出错代码。**



参考资料

1、为什么linux内核函数出现错误，返回值是一个负数

https://blog.csdn.net/zhangzheng_1986/article/details/81705572