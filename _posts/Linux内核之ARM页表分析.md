---
title: Linux内核之ARM页表分析
date: 2018-03-18 11:11:46
tags:
---

1

Linux在启动之初会建立临时页表，但是在start_kerne函数中setup_arch又会建立正真的页表和页目录。

临时页表建立的空间和正式页表建立的空间分别部署于不同的空间，因此不会出现覆盖或者修改等现象。

arm linux使用两级页表，L1是pgd，L2是pte。

其中L1页表共2048项，每项占用8bytes，每项对应2M内存，共占用2048*8=16K bytes。

arch/arm/include/asm/pgtable-2level.h



arm为什么要先建立临时页表？起什么作用？

kernel启动阶段，还没有使能mmu。**所以在使能mmu之前，应该让kernel的代码能够与位置无关。**



Linux启动分为2个阶段：

1、汇编代码里建立一个临时页表进入分页机制。

2、C语言里初始化系统资源。



不管在临时页表机制，还是后面的正式页表机制里，Linux是不需要把内核自身的代码段、数据段这些映射到页表里的。

在进入正式页表机制之前，Linux需要一个临时的页表来管理低端内存。



鉴于arm 32位的页表，只有两级页表，相对来说比较简单，所以我现在以这个情况为突破口。

把Linux页表理解透彻。

是不是可以用目录层次来辅助理解多节页表呢？

假如只有一级页表，一页是4K，对于4GB内存，就是大概100万个条目。

想象一下，在一个文件夹下面，之间放了100万个文件，是什么感觉。

如果是两级页表，那么相当于第一层目录，下面放了1024个子目录。

每个子目录下，分别放了1024个文件。

这样看起来感觉就好多了。

你只有打开某个子目录的时候，才需要去磁盘里去查询该子目录下的文件。其他子目录的你完全不用管。

对于系统的负担也是很大的减轻。



arm的第一级页表条目数为4096个，对于4K页第二级目录条目个数为256个，一级二级条目都是每个条目4字节。

在linux下二级分页如下：虚拟地址——> PGD转换——> PTE转换——>物理地址。

arm-linux假装第一级目录只有2048个条目，但其实每个条目是2个ulong大小即8字节，所以最终设置MMU的还是4096个条目，只是每访问1个pgd条目将可以访问到2个pte条目，linux为了实现其内存管理功能又在后面加上2个对应的假pte表，这个假pte表专门给linux内核代码自己用的，不会影响arm硬件(事实上还有一个重要原因是，linux要求pte表长度为4K即一页)。

```
typedef unsigned long pte_t;
typedef unsigned long pmd_t;
typedef unsigned long pgd_t[2];
typedef unsigned long pgprot_t;
```



Linux的正式页表，是在start_kernel函数里的paging_init函数里创建的。

paging_init函数可以正常创建内存页表的条件有2个：

1、meminfo已经初始化。就是各个node的各个bank都已经初始化了。在嵌入式里，一般是一个node，一个node里只有一个bank。

2、全局变量init_mm的text_begin、text_end、data_begin、data_end这4个成员已经初始化。

界定这4个变量的意义在于：可以得出内核运行需要的空间的位置和大小。



prepare_page_table

这个函数是清除临时页表。代码的注释是这么写的。

内核我们一般放在类似80008000这种位置，前面8000 0100 这里放boot参数。

8000 4000 这里开始，放的是16K的临时页表。

现在就是要把这个临时页表清除掉。

```
/*
	 * Clear out all the mappings below the kernel image.
	 */
```



什么是内存页表？

有哪些属于内存？

对于soc，有些寄存器也在页表的管理之下的。

具体来说，内存页表，叫内存映射其实更能反映实际情况。

对于带有mmu的cpu来说，cpu要访问物理内存或者某个soc寄存器的时候，并不是直接把地址放到了cpu的地址总线上。

而是把一个虚拟地址交给mmu。

如果mmu硬件里存在这个虚拟地址对应的物理地址，那么mmu就把对应的物理地址放到cpu的地址总线上。

这样做的好处是：

1、避免了用户程序直接访问一个不存在的地址而破坏系统。

2、用户程序可以使用的内存看上去很大。



所有通过cpu地址总线连接的东西，都可以被映射。

函数create_mapping是最终创建内存映射的函数。看看这个函数，被3个地方调用了：

1、map_memory_bank。这个是物理内存的映射。

2、devicemaps_init：这个是中断向量的映射。

3、iotable_init：这个是soc硬件寄存器的映射。



create_mapping 这个函数是关键。

接收一个参数：struct map_desc类型。

这个结构体，4个成员。

前面三个分别是：虚拟地址、物理了地址、长度。

第四个是类型：

我们只用这几种：MT_DEVICE（寄存器映射）、MT_MEMORY（物理内存）、MT_HIGH_VECTORS（中断向量）。



具体创建映射是怎么做的呢？

32位的arm芯片寻址空间是2^32，就是4GB。

如果按照1M大小为单位进行映射，就需要4096个条目。

每个条目负责1M的地址范围。

如果映射一个128M的物理内存，只需要128个条目就够了。

这个就是一级页表。

优点：

条目较少，4096个，每个条目4字节，一个进程的页表只需要占用16K的空间。

缺点：

粒度太大了，不便于Linux内存管理。

即使你用不了1M的空间，也只能申请1M的。

所以这个缺点是不能容忍的。

必须改进。

所以引入了二级页表。



每个进程都有一个自己的mm_struct，来描述自己的内存使用情况。

内核进程也是如此。



```
struct mm_struct init_mm = {
	.mm_rb		= RB_ROOT,
	.pgd		= swapper_pg_dir,
	.mm_users	= ATOMIC_INIT(2),
	.mm_count	= ATOMIC_INIT(1),
	.mmap_sem	= __RWSEM_INITIALIZER(init_mm.mmap_sem),
	.page_table_lock =  __SPIN_LOCK_UNLOCKED(init_mm.page_table_lock),
	.mmlist		= LIST_HEAD_INIT(init_mm.mmlist),
	.cpu_vm_mask	= CPU_MASK_ALL,
};
```

我们看看swapper_pg_dir这个。

在C000 4000这个位置，因为KERNEL_RAM_VADDR是C000 8000。

```
./arch/arm/kernel/head.S:45:    .equ    swapper_pg_dir, KERNEL_RAM_VADDR - 0x4000
```

在System.map里也可以看到。

```
c0004000 A swapper_pg_dir
c0008000 T __init_begin
c0008000 T _sinittext
c0008000 T _stext
c0008000 T stext
c0008034 t __enable_mmu
```

所以内核的内存页表的虚拟地址范围是c000 4000到c000 8000 。大小是16K。

内核的内存页表，都映射了一些什么内容呢？

根据前面的介绍，就是3个部分：物理内存、中断向量、寄存器。



除了看Linux内核里对页表的处理，还需要看arm的页表逻辑跟内核的页表逻辑的融合。

因为二者的机制不完全一致，需要互相匹配。

arm体系结构的MMU实际上支持两级页表。





参考资料

1、ARM-Linux （临时，正式） 建立页表的比较

https://blog.csdn.net/edwardlulinux/article/details/38967521

2、arm linux 临时页表的建立

https://blog.csdn.net/flaoter/article/details/73381695

3、arm页表在linux中的融合

https://www.cnblogs.com/yangjiguang/p/8245306.html

4、arm-linux内存页表创建

这篇文章讲得很细了。值得反复读。

https://blog.csdn.net/waterhawk/article/details/49175973

5、ARM中的linux页表与硬件页表（linux4.0）

https://blog.csdn.net/geshifei/article/details/89574508

6、linux启动过程中建立临时页表

https://www.cnblogs.com/4a8a08f09d37b73795649038408b5f33/p/10154324.html