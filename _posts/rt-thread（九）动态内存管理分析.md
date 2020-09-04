---
title: rt-thread（九）动态内存管理分析
date: 2018-02-03 15:25:06
tags:
	- rt-thread
typora-root-url: ..\
---

1

里面有几个东西看起来像是heap。

有mem.c、memheap.c、slab.c。

mem.c：默认的动态内存管理。需要下面2个宏同时满足。

```
#if defined (RT_USING_HEAP) && defined (RT_USING_SMALL_MEM)
```

可见，这个是适合管理比较小的内存。

memheap.c：目前只在ramfs里用到。

也可以把memheap.c作为默认的动态内存管理。

需要打开下面这个宏。

```
RT_USING_MEMHEAP_AS_HEAP
```

slab.c

这个应该适合管理比较大的内存。需要下面2个宏同时满足。

```
#if defined (RT_USING_HEAP) && defined (RT_USING_SLAB)
```



rt-thread默认用的是mem.c里的代码。

1、先要看一下heap_mem这个结构体。4个成员。一共12个字节。

这个是内存管理的单元。所以只分配1个字节，实际上用消耗16个字节。所以分配太小的内存，效率比较低。

```
    rt_uint16_t magic; 魔数。0X1EA0
    rt_uint16_t used; 这个肯定是表示被占用。

    rt_size_t next, prev; 相当于指针。
```

2、入口函数。rt_system_heap_init。

```
为了便于分析，我们给定一组简单的值，套入进行分析。
1、begin为0x100（256），end为0x200（512） 。
2、对齐后的memsize就是512 - 256 -2*12 = 232字节。
3、
```

函数执行完之后的内存情况如下图。

![rt-thread（七）-1](/images/rt-thread（七）-1.png)

3、我们rt_malloc 12个字节看看。

![rt-thread（七）-2](/images/rt-thread（七）-2.png)



也不复杂。









