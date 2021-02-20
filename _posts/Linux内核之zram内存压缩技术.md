---
title: Linux内核之zram内存压缩技术
date: 2021-02-19 16:28:30
tags:
- Linux
---

--

# 什么是内存压缩

就是对内存里暂时不用的数据，进行压缩，减少内存占用。



# 为什么要进行内存压缩

尽管当前android手机6GB，8GB甚至12GB的机器都较为常见了，

但内存无论多大，总是会有不够用的时候。

当系统内存紧张的时候，

会将文件页丢弃或回写回磁盘（如果是脏页），

还可能会触发LMK杀进程进行内存回收。

这些被回收的内存如果再次使用都需要重新从磁盘读取，

而这个过程涉及到较多的IO操作。

就目前的技术而言，IO的速度远远慢于这RAM操作速度。

因此，如果频繁地做IO操作，

不仅影响flash使用寿命，还严重影响系统性能。

内存压缩是一种让IO过程平滑过渡的做法, 

**即尽量减少由于内存紧张导致的IO，提升性能。**

# 内存压缩有哪些方式

目前linux内核主流的内存压缩技术主要有3种：zSwap, zRAM, zCache。

## zswap

zSwap是在memory与flash之间的一层“cache”,

当内存需要swap出去磁盘的时候，

先通过压缩放到zSwap中去，zSwap空间按需增长。

达到一定程度后则会按照LRU的顺序(前提是使用的内存分配方法需要支持LRU)

将就最旧的page解压写入磁盘swap device，之后将当前的page压缩写入zSwap。



zswap本身存在一些缺陷或问题:

1) 如果开启当zswap满交换出backing store的功能, 由于需要将zswap里的内存按LRU顺序解压再swap out, 这就要求内存分配器支持LRU功能。

2) **如果不开启当zswap满交换出backing store的功能, 和zRam是类似的。**

## zram

zram即压缩的内存， 

使用内存模拟block device的做法。

实际不会写到块设备中去，

只会压缩后写到模拟的块设备中，其实也就是还是在RAM中，只是通过压缩了。

**由于压缩和解压缩的速度远比读写IO好，因此在移动终端设备广泛被应用。**

zRam是基于RAM的block device, 一般swap priority会比较高。

只有当其满，系统才会考虑其他的swap devices。当然这个优先级用户可以配置。



zRram本身存在一些缺陷或问题:

1) zRam大小是可灵活配置的, 那是不是配置越大越好呢? 如果不是,配置多大是最合适的呢?

2) 使用zRam可能会在低内存场景由于频繁的内存压缩导致kswapd进程占CPU高, 怎样改善?

3) 增大了zRam配置,对系统内存碎片是否有影响?

要利用好zRam功能, 并不是简单地配置了就OK了, 还需要对各种场景和问题都做好处理, 才能发挥最优的效果。

## zcache

zCache是oracle提出的一种实现文件页压缩技术，

也是memory与block dev之间的一层“cache”,

与zswap比较接近，**但zcache目前压缩的是文件页**，而zSwap和zRAM压缩是匿名页。



zcache本身存在一些缺陷或问题:

1) 有些文件页可能本身是压缩的内容, 这时可能无法再进行压缩了

2) zCache目前无法使用zsmalloc, 如果使用zbud,压缩率较低

3) 使用的zbud/z3fold分配的内存是不可移动的, 需要关注内存碎片问题



# 配套的malloc算法

## zsmalloc

zsmalloc是为ZRAM设计的一种内存分配器。

内核已经有slub了， 为什么还需要zsmalloc内存分配器？

这是由内存压缩的场景和特点决定的。

zsmalloc内存分配器期望在低内存的场景也能很好地工作，

事实上，当需要压缩内存进行zsmalloc内存分配时，

内存一般都比较紧张且内存碎片都比较严重了。

如果使用slub分配， 很可能由于高阶内存分配不到而失败。

另外，slub也可能导致内存碎片浪费比较严重，

最坏情况下，当对象大小略大于PAGE_SIZE/2时，每个内存页接近一半的内存将被浪费。

## zbud

# 压缩算法

可以看到，使用lz4压缩算法，效率是最高的。

![wps2D14.tmp](http://www.wowotech.net/content/uploadfile/202003/d6e53e3fe37da3c00a4a16cfcaa1922620200308003818.jpg)



# 参考资料

1、zRAM内存压缩技术原理与应用

http://www.wowotech.net/memory_management/zram.html