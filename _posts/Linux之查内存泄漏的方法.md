---
title: Linux之查内存泄漏的方法
date: 2019-12-12 13:56:38
tags:
	- Linux

---

1

在内核里，128K以内的分配，用brk。128K以上的，用mmap来做的分配。

brk对应的用户态库函数是sbrk。

用法是这样：

```
void *ptr = sbrk(1);//分配一个字节的内存。
```



```
#include <unistd.h>
int brk(void *addr);
void *sbrk(intptr_t increment);
```



brk实际上是把heap的顶端往上移动。

所以可以通过sbrk的值，来检查内存是否有泄漏。如果sbrk的值一直增大，则说明内存在泄漏。

可以把系统的malloc替换为自己写的，在里面加内容来统计内存使用情况。

sbrk的体现是RSS值。这个可能不能准确反映内存泄漏的情况。

因为C语言glibc的内存管理，从操作系统申请内存的时候，有2种方式：sbrk() 向上线性扩展虚拟地址空间, mmap匿名内存映射文件分配虚拟地址空间； 前者对应小块内存分配，后者满足大块内存分配。



参考资料

1、一次由于sbrk()无法压缩导致内存RSS虚高造成“内存泄露”的假象

<http://chenzhenianqing.com/articles/1061.html>

2、Linux虚拟内存介绍，以及malloc_stats和malloc_info 监控查看内存情况

<https://blog.csdn.net/zzhongcy/article/details/89135056>