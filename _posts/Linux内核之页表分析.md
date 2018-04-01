---
title: Linux内核之页表分析
date: 2018-03-13 13:31:14
tags:
	- Linux
typora-root-url: ..\
---



# 缩写

PGD：Page Global Directory

PUD：Page Upper Directory

PMD：Page Middle Directory

PTE：Page Table Entry

```
typedef pteval_t pte_t;
typedef pmdval_t pmd_t;
typedef pmdval_t pgd_t[2];
typedef pteval_t pgprot_t;
```

val_t的，都是u32的。所以都是u32的。

使用二级页表的话，PGD==PMD。



Linux在启动之初，会建立临时页表，后面再start_kernel函数里又会建立真正的页表和页目录。

![Linux内核内存分布](/images/Linux内核内存分布.png)

绿色部分的pgd是内核0号进程的主页表。

ko的那16M在代码里是这样的：

```
#define MODULES_VADDR		(PAGE_OFFSET - 16*1024*1024)
```



# 内存布局的演进

代码要在ram里运行，有3个基本要素：

1、代码。

2、全局数据。

3、堆栈。

所以可以把内存简单地分为这3个区域。在单片机上就是这么做的，有些dsp也是这么做的。

优点的简单，确定是只能运行一个程序。



然后随着应用越来越复杂，现在需要运行多个程序了。

程序用分时复用的方式来使用CPU。

为了管理多个程序的切换，就需要增加全局的代码，就是os了。



每个程序都有属于自己的代码、数据、堆栈，但是问题是，不同的程序在运行时需要的数据和堆栈空间是不一样的。

如何给系统中的程序分配内存就成了一个问题。给多大是合适的。不好定。

所以就引入了虚拟内存的概念。



# arm的内存映射表

主要讲解armv7的硬件如何支持内存映射。

armv7上支持两种内存管理：

1、VMSA。过时。淘汰了。

2、PMSA。主流。

首先要有一个地址映射表。

ARM处理器默认是关闭这个功能的，因为CP15里的TTBR寄存器，默认是0 。

表示系统里没有有效的虚拟内存映射表。

也就是说，arm不知道该如何进行地址映射。

这个决定权是交给了os。



ARMv7的映射表支持2种结构。

1、为32位系统设计的。short descriptor format。

2、为64位系统设计。long descriptor format。

armv7之前，没有对64位进行支持。下面主要用32位的来讲解。



虚拟映射表包含二级。一级表是必选，二级表是可选的。

一级表支持2种格式：

1、一种叫做section，映射1M的空间。对应的二级页表有256个表项。每个表项对应4K。

2、一种叫supersection。映射16M的空间。对应的二级页表有256个表项。每个表项对应64K。

目前一般使用section 加small page的配置方式。就是第一种方式了。



os在初始化映射表的时候，没有被使用的表项会被设置为0 。

arm的mmu单元在翻译一个虚拟地址的时候：

1、把虚拟地址的高12位作为索引来定义在一级页表里的表项。

2、如果表项的内容是0，那么说明这个虚拟地址还没有被映射到某个物理内存。

3、这时候，mmu硬件会产生一个异常，迫使CPU进入到data abort这个异常模式来处理。

4、如果表项是有效内容。mmu会进一步判断，表项内容的最低2位，如果是01，表示是二级页表地址。如果是10，则是指向1M的连续内存。



![ARMLinux内存映射](/images/ARMLinux内存映射.png)



在mmu使能的系统里，物理内存的分配和释放都是通过这个表来完成的。

虽然这个表在内存里，但是它的格式是ARM定义的。

这个表是给MMU硬件用的。表的内容是生产者是os。

os在管理物理内存的过程中，不断地在做这些事情：

1、不断地配置不同的虚拟映射表到arm的TTBR0里，达到切换进程的目的。

不同进程的映射表不同。

2、不断地修改一级页表、二级页表的表项，实现内存的分配和释放。



```
中断vector的位置，默认是在0这里，也是CP15里的寄存器配置，某个位为1，则会放到0xFFFF 0000这里。
一般都会这么做，这样位置0，就可以被当成无效指针来定义了。
```



Linux下的页表映射分为两种：

1、Linux自身的页表映射。

2、ARM的MMU的硬件的映射。

由于arm和linux的页表项不同，所以维护了两套PTE。



arm硬件上，二级页表：

1、 高12位，4K个条目。

2、 中间8位，256个条目。

Linux实现上，是三级页表结构，硬件无关。

三级的实现对接到二级的页表，就是只用PGD和PTE。PMD不用就好了。

读pgtable-2level.h里的注释。

L_PTE_xxx是Linux的。

PTE_xxx是arm的。

```
/*
 * "Linux" PTE definitions.
 *
 * We keep two sets of PTEs - the hardware and the linux version.
 * This allows greater flexibility in the way we map the Linux bits
 * onto the hardware tables, and allows us to have YOUNG and DIRTY
 * bits.
 *
 * The PTE table pointer refers to the hardware entries; the "Linux"
 * entries are stored 1024 bytes below.
 */
```

CONFIG_PGTABLE_LEVELS=2 配置的页表分级是二级的。

使用二级页表，就是为了节省空间。
因为大多数进程不会用到整个虚拟内存空间。
所以虚拟内存空间会留下很多的空洞。
采用二级页表，只要第一级的某项是空的，那么它对应的1024个page desc就可以省掉了。
这个空间就省出来了。
当地址宽度是32位的时候，二级页表是合适的。
当地址宽度是64位的时候，二级页表就不够有效了。
而Linux内核设计要考虑到64位的CPU。
所以它的设计是基于一种假象的CPU和mmu来进行的。
所以把映射机制设计成了3级，pgd、pmd、pt。pt里面的条目就是pte。
pgd、pmd、pt都是数组。
然后，对应地，把一个线性地址的32bit划分为4个部分：
1、pgd里的下标。
2、pmd里的下标。
3、pt里的下标，就是对应的pte。
4、在pte对应页里面的偏移。

理论上，系统最大的进程数是4090个。
在我的64位虚拟机上，是这么多。
max user processes              (-u) 15575

与段式管理相比，页式管理有很多好处：
1、页面大小是固定的，便于管理。
在把页面换出到磁盘的时候，段一般很大，而页比较小。
效率会高很多。
一种CPU既然支持页式管理，就没有必要用段式管理了。
x86是因为历史原因遗留的段式管理。

主动的中断，就叫trap。

# 特殊的零页

零页是要特别构建的，就像0号进程一样。



# linux内核的物理内存管理

固定映射区域，也就低端内存。

特点有：

1、在内核里使用内存，不要进行映射和解除映射的操作。因为固定映射区域的映射是一直存在的。所以才叫固定映射。

2、如果App申请的物理内存在固定映射区域内，需要把这块内存映射到用户空间。一块内存被映射了2次。



对于固定映射区域，就可以不用二级页表。

因为：

1、映射的区域具有相同的访问权限。

2、固定的 ，不需要解除。

3、内核空间在动态申请的时候，也是以4K为单位的。



对于CPU来说，进程和线程没有本质区别。

进程是一个逻辑概念，线程才是CPU执行的主体。



对于内存来说，进程和线程的本质区别就是：不同的进程，有不同的内存映射表。



前面我们看到，arm的页表分级是二级。

在linux里是如何处理的呢？

有3个概念。

pgd。相当于把相邻的2个section当成一个整体。例如section[0]和section[1]

pmd。每个section就是一个pmd。

pte。就是一个small page。



#从linux代码来看

重点看：

```
setup_arch
build_all_zonelists
mm_init
```

这3个函数。

在mm_init结束后，buddy系统才可以用。在这里之前，内核是用memblock来管理内存的。



paging_init可以正常创建内存页表的条件有2个。

1、meminfo已经初始化。对于一般的小型arm嵌入式系统，只有一块内存，就对应一个node和一个bank。

2、全局变量init_mm



# buddy和slab的关系

buddy分配大块内存用的。

slab是分配小块内存用的。





# 参考文章

1、Linux页表机制分析

https://wenku.baidu.com/view/0429c0702f60ddccda38a0c9.html

2、基于ARM CPU的Linux物理内存管理

对于内存布局管理的来由讲得很清楚。值得反复读。

https://wenku.baidu.com/view/2a51be93856a561252d36ff5.html

3、Linux内存管理_陈莉君

https://wenku.baidu.com/view/2d2da4747c1cfad6185fa742.html

4、Linux内存管理

https://wenku.baidu.com/view/3d52eb6b58fafab069dc0254.html

