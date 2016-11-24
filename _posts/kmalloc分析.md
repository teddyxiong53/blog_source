---
title: kmalloc分析
date: 2016-11-04 21:42:55
tags:
	- kmalloc
---
kmalloc的特点：
1. 速度快，不清零获取到的内存。
2. 获取的内存在物理上是连续的。
函数原型是：
```
#include <linux/slab.h>
void *kmalloc(size_t size, int flags);
```
下面我们重点看看flags这个参数。它用来控制kmalloc的行为。
* GFP_KERNEL。这个是最常用的一个标志。这个标志意味着当前进程在当前没有空闲内存的时候，会进入到睡眠状态来等待一会儿，让内核想办法来腾出一些内存来用。所以使用这个标志来kmalloc，不能在原子上下文里进行。
* GFP_ATOMIC。这个就跟GFT_KERNEL相对应，不会进入睡眠，暂时分不到就返回失败。一般用在中断里。
* GFP_USER。为用户空间页分配内存，可能睡眠。
* GFP_HIGHUSER。从高端内存分配。


