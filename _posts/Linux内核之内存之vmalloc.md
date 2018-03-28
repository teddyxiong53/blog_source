---
title: Linux内核之内存之vmalloc
date: 2018-03-13 15:27:39
tags:
	- Linux

---



当buddy系统还有大量的连续内存的时候，我们可以通过`__get_free_pages`来分配一大块连续的物理内存。

随着系统的运行，内存变得不连续，就很难得到一大块连续的物理内存了，这个时候还用`__get_free_pages`来做的话，就会分配失败。

实际上，除了DMA操作外，其他的地方都是不需要连续的物理内存的。



kmalloc和__get_free_pages得到的内存都是物理地址连续的。

vmalloc的则线性地址连续，物理地址不连续。



vmalloc的一个典型用途就是在create_module系统调用里用。

vmalloc比__get_free_pages开销要大很多，会导致新的页表建立。

所以要用，就用在需要分配较大内存的地方，分配小内存划不来。



kmalloc的底层 就是slab。

slab的底层还是get_free_pages，slab每次申请一页或者多页，然后进行切分再用。



vmalloc相关的一个结构体是struct vm_struct。

```
vm_struct和vm_area_struct区别
1、vm_struct是内核虚拟地址空间映射。
	vm_area_struct是应用进程虚拟地址空间映射。
2、vm_struct不会产生page fault，而vm_area_struct一般不会提前分配页面，只有当访问的时候，产生page fault来分配页面。
```

vmalloc分配可能会阻塞。







# 参考资料

1、

http://blog.csdn.net/av_geek/article/details/41249267

