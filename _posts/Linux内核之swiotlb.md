---
title: Linux内核之swiotlb
date: 2020-04-17 16:28:01
tags:

	- Linux

---

--

看rk3308的启动参数里，有一个：

```
swiotlb=1
```

这个是什么意思呢？

在kernel/lib/swiotlb.c里，注释里写着：

```
 Dynamic DMA mapping support.
```

```
 * This implementation is a fallback for platforms that do not support
 * I/O TLBs (aka DMA address translation hardware).
```

是给不支持dma地址硬件翻译的平台使用的。

这个词拆开来是这样：

sw：代表软件。

io：就是io。

tlb：

swiotlb技术是一种纯软件的技术。主要是给寻址能力受限的dma提供软件上的代码映射。

为什么会出现这种技术呢？

我们先看一个应用场景。

假设有一个64位的系统，它的内存基地址是0x8000 0000，内存大小是4G。

那么内存地址就是：0x8000 0000到0x18000 0000。

同时，系统里有一个dma硬件，只能进行32位的空间寻址。

如果分配给这个dma硬件的内存地址，超过了32位的寻址空间。那么如果没有什么特别处理，dma硬件是用不了分配的内存的。

那怎么呢？swiotlb就是用来解决这个问题的。

swiotlb维护了一块低地址的buffer。

这个buffer的大小，可以由bootloader通过swiotlb参数传递给kernel。也可以使用默认值，默认值是64M。





参考资料

1、Linux swiotlb技术解析

https://blog.csdn.net/liuhangtiant/article/details/87825466