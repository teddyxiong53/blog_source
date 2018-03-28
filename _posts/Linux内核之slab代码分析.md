---
title: Linux内核之slab代码分析
date: 2018-03-13 13:27:29
tags:
	- Linux内核

---



我主要是做嵌入式，嵌入式一般是用slob。

slob应该也是slab、slub、slob这3个里最简单的。



slob是Simple List Of Blocks的缩写。

slob是一个传统的K&R/unix堆分配器。比slab代码更精简，效率更高，但是产生碎片的概率比slab高。

所以只适合在嵌入式系统里用。



slob分配器总共只有三条半满空闲链（partial free list）：

1、free_slab_large。分配小于4K的块。

2、free_slab_medium。分配小于1024字节的块。

3、free_slab_small。分配小于256字节的块。

每个list都是由分配给slob的page组成。

如果通过slob分配大于4K的块，slob会直接调用alloc_pages分配页并返回。

```
#define SLOB_BREAK1 256
#define SLOB_BREAK2 1024
```



# 参考资料

1、LINUX内核狂想曲之SLOB分配器

https://www.cnblogs.com/icanth/archive/2012/05/20/2510742.html

