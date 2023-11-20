---
title: Linux内存（二）
date: 2018-01-23 21:28:45
tags:
	- Linux内存

---



在内核基本完成内存初始化之后，整体布局稳定之后，`start_kernel-->mm_init-->mem_init`会打印一段内存layout。

vexpress的打印如下：

```
Memory: 1031428K/1048576K available (4787K kernel code, 156K rwdata, 1364K rodata, 1348K init, 166K bss, 17148K reserved, 0K cma-reserved, 270336K highmem)
Virtual kernel memory layout:
    vector  : 0xffff0000 - 0xffff1000   (   4 kB)
    fixmap  : 0xffc00000 - 0xfff00000   (3072 kB)
    vmalloc : 0xf0000000 - 0xff000000   ( 240 MB)
    lowmem  : 0xc0000000 - 0xef800000   ( 760 MB)
    pkmap   : 0xbfe00000 - 0xc0000000   (   2 MB)
    modules : 0xbf000000 - 0xbfe00000   (  14 MB)
      .text : 0xc0008000 - 0xc060a09c   (6153 kB)
      .init : 0xc060b000 - 0xc075c000   (1348 kB)
      .data : 0xc075c000 - 0xc07833c0   ( 157 kB)
       .bss : 0xc07833c0 - 0xc07acbf0   ( 167 kB)
```

上面这些地址都是虚拟地址，其中lowmem是线性映射区。

.text、.init、.data、.bss都属于lowmem区域，也就是ZONE_NORMAL。

vector、fixmap、vmalloc都属于ZONE_HIGHMEM区域。

pkmap、modules属于用户空间。



为什么kernel image（.text）空间从0xc000 8000开始呢？

0xc000 8000 = PAGE_OFFSET + TEXT_OFFSET。

这个在arch/arm/kernel/vmlinux.lds.S里进行了明确定义。

```
. = PAGE_OFFSET + TEXT_OFFSET;
	.head.text : {
		_text = .;
		HEAD_TEXT
	}
```



# vmalloc空间

vmalloc用来给vmalloc、ioremap分配内存。

vmalloc空间的确定方法很简单：

1、先确定vmalloc 终点位置0xff00 0000。我看这个地址不同的板子不同。

2、然后是确定vmalloc的起点。vmalloc和lowmem中间要一个8M的Gap。这个Gap用于捕获虚拟地址的越界访问。

vmalloc_min的最小值是vmalloc_end的值减去240MB。

