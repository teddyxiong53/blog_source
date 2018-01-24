---
title: Linux内存（一）
date: 2018-01-23 18:19:01
tags:
	- Linux
typora-root-url: ..\
---



对应的文件在Documentation/arm/memory.txt里。

| 开始            | 结束            | 用途                                  |
| ------------- | ------------- | ----------------------------------- |
| FFFF 8000     | FFFF FFFF     | 用于copy_user_page和clear_user_page    |
| FFFF 4000     | FFFF FFFF     | armv6及之后的CPU的cache混淆。               |
| FFFF 1000     | FFFF 7FFF     | 保留。不能用。                             |
| FFFF 0000     | FFFF 0FFF     | CPU vector页。如果CPU支持vector重定位，映射到这里。 |
| FFFE 0000     | FFFE FFFF     | XScale缓存冲刷区。这种CPU没有TCM              |
| FFFE 8000     | FFFE FFFF     | 各个平台的DTCM映射区。                       |
| FFFE 0000     | FFFE 7FFF     | 各个平台的ITCM映射区。                       |
| FFC0 0000     | FFEF FFFF     | 固定映射区。调用fix_to_virt函数分配该区域。         |
| FEE0 0000     | FEFF FFFF     | PCI io映射看空间。是vmalloc空间的静态映射。        |
| VMALLOC_START | VMALLOC_END-1 | vmalloc、ioremap空间。                  |
| PAGE_OFFSET   | high_memory-1 | 内核直接映射内存区。所有平台典型的一一映射关系。            |
| PKMAP_BASE    | PAGE_OFFSET-1 | 内核持久映射区。                            |
| MODULES_VADDR | MODULES_END-1 | 内核模块映射空间。                           |
| 0000 0100     | TASK_SIZE-1   | 用户进程映射区。每个进程通过mmap映射到这个区域。          |
| 0000 0000     | 0000 0FFF     | CPU向量页。                             |

整个内存管理从宏观上可以分为三大部分：用户空间、内核空间和相关硬件。

用户空间主要是libc对相关系统调用进行封装。对用户提供的接口就是malloc、mmap这些。

相关硬件包括mmu等。

内核空间就复杂多了。先看看初始化以及初始化之后的布局。

linux内存管理框架图。

![](/images/linux内存管理框架图.png)

下面代码的分析基于linux 4.4的版本。

内核启动过程中设计到的内存相关函数调用情况：

```
start_kernel-->
	page_address_init
	setup_arch
		paging_init
	mm_init
	kmemleak_init
	
```

当配置为3G/1G的内存配置的时候，在autoconf.h里就生成了：

```
#define CONFIG_PAGE_OFFSET 0xc0000000
```

一切内存初始化和管理都是基于物理内存，所以首先要得到物理内存的起始地址和大小。

这个是在设备树里配置的。

```
arch/arm/boot/dts/vexpress-v2p-ca9.dts

memory@60000000 {
        device_type = "memory";
        reg = <0x60000000 0x40000000>;
    };
```

得到起始地址是0x6000 0000，size是1GB。

```
early_init_dt_scan_memory
	early_init_dt_add_memory_arch(base, size)
		memblock_add(base, size)
```



在内核启动阶段，也有内存管理的需求，但是这个时候伙伴系统还没有完成初始化。是使用memblock作为内核初始化阶段内存分配器。之前的内核是用bootmem机制。现在内核还是遗留了这个配置项的。不过arm架构的默认都关闭bootmem这个机制的。



arm32没有打开CONFIG_ARM_LPAE（large physical address extension），linux页表采用两层映射。

四层映射是：

```
PGD->PUD->PMD->PTE
```

两层映射的时候，PUD和PMD被省掉了。

prepare_page_table用来清空页表项。实际上清空了三段地址的页表项，分别是：

1、0到modules_vaddr

2、modules_vaddr到page_offset

3、0xef800000到vmalloc_start。

真正创建页表是在map_lowmem创建了两块区域。

1、0x6000 0000到0x6080 0000（0xc000 0000到0xc080 0000）。有rwx权限。主要存放kernel代码段数据段。

2、0x6080 0000到0x8f80 0000 （0xc080 0000到0xef80 0000）。rw权限，没有x权限。是Normal Memory部分。

可以看出这2个区虚拟地址到物理地址的映射是线性映射的。但是在末尾存在特殊的两页不是线性映射。

还有一部分内存映射在devicemaps_init里进行，用来对vectors进行映射。

MT_HIGH_VECTORS：

虚拟地址：0xFFFF 0000到0XFFFF 1000，对应的物理地址是0X8F7F E000到0X8F7F F000。

MT_LOW_VECTORS：

虚拟地址是0XFFFF 1000到0XFFFF 2000，对应的物理地址是0X8F7F F000到0X8F80 0000。



内存管理把一个内存Node分成多个Zone进行管理。

Zone的类型在enum zone_type里定义。

vexpress只定义了NORMAL和HIGHMEM这两种。

仔细分析对应的bootmem_init，计算出ZONE_NORMAL就是0x6000 0000到0x8f80 0000.

ZONE_HIGHMEM 就是0X8F80 0000到0xa000 0000 。





