---
title: 《ARM Linux内核源码剖析》读书笔记
date: 2018-03-01 12:40:06
tags:
	- 笔记
	- Linux
typora-root-url: ..\
---



# 1. 2.6和3.0版本内核差异

2011年7月，Linux内核3.0版本发布，2.6版本是2003年首次发布的。从版本2过渡到版本3，花了8年的时间。

下面罗列2.6.30到3.2版本的主要变更点。

##2.6.31

1、添加对usb3.0的支持。

2、添加了cuse。character device in userspace。

3、添加了performance counter子系统。

4、添加了kmemcheck功能。

## 2.6.32

1、优化了btr文件系统。

2、添加了kernel samepage merging功能。

3、添加了runtime 电源管理功能。

## 2.6.33

1、去除了对Android的支持。

2、添加了compcache。

3、添加了brbd。

4、添加了系统调用函数recvmmsg。

## 2.6.34

1、添加了log文件系统。

2、添加了Ceph文件系统。

3、添加了rcu lockdep功能。

## 2.6.35

1、添加了memory compaction的实现。

2、添加了对L2TP的支持。

## 2.6.36

1、添加了对Tile处理器的支持。

2、并发管理workqueue。

3、重写了oom。

## 2.6.37

1、优化ext4的扩展性和mkfs速度。

2、优化了xfs的扩展性。

3、从核心性能的内核代码去掉了所有的BKL（大内核锁）。但是driver和ioctl中还无法去除。

## 2.6.38

1、添加了使用session id自动集成process的功能。

2、改了vfs的扩展性。

3、添加了transparent huge pages功能。

## 2.6.39

1、默认根据2.6.37的ext4改善配置。

2、去除了所有的BKL代码。

## 3.0

1、防止自动整理btr文件系统，添加了scrubbing功能的同时改善了性能。

2、添加了系统调用函数sendmmsg。

3、添加了对XEN dom0的支持。

4、添加了用于改善page cache性能的clear cache。

5、添加了Berkeley packet filter。

## 3.1 

1、添加了对OpenRISC处理器的支持。

2、改善了writeback的性能。

3、改善了slab的性能。

## 3.2

1、优化ext4.

2、去除cfs中的cpu带宽限制。

3、添加了对Hexagon处理器的支持。



从上面这些来看，系统没有根本性的大变动。

我们可以从内核2.6版本进行学习。



# 2. 内核build系统

##vmlinux的镜像分布

```
arch/arm/kernel/head.o
arch/arm/kernel/init.o
init/
kernel/
mm/
fs/
ipc/
security/
...
```

## 生成zImage的过程

![ARMLinux内核源码剖析1](/images/ARMLinux内核源码剖析1.png)



# 3. 了解arm处理器

1、1985年，Acorn公司首次对ARM处理器进行商用化运作。ARM是Advanced RISC Machine的缩写。

2、arm处理器以Berkeley RISC架构为基础。其risc特性如下：

```
1、指令。指令种类少。
2、管道。通过管道执行时，一边解码当前指令，一边取得下一条指令。
3、load store结构。
```

## arm处理器版本

arm架构和arm核心

arm架构就是ARMv4这样的。

arm核心，就是cortex M、Cortex A这些。

## arm的硬件扩展功能

1、arm处理器，就是向arm核心添加硬件扩展功能得到的。

2、扩展功能有cache、mmu、协处理器。

## gcc中对arm寄存器的命名

arm寄存器是从r0到r15，这个名字的含义不明确。gcc另外定义了一套名字，跟这个一一对应。

```
r0到r3：被叫做a1到a4，a表示arg参数。依次放函数的第一到四这4个参数。r0还多一个功能，就是放返回值。
r4到r9：被叫做v1到v6 。v表示变量。
r10：sl。栈界限stack limit。
r11：fp。frame pointer。
r12：ip。scratch pointer。
r13: sp
r14: lr
r15: pc
```



# 4. 内核的启动

1、分析的开始文件是arch/arm/boot/compressed/head.S。

从这里的start标签开始看。

一开始就把机器码和atags保存到r7和r8寄存器。

```
1:		mov	r7, r1			@ save architecture ID
		mov	r8, r2			@ save atags pointer
```

然后就是禁止中断，

然后是设置r1到r6，以及ip和sp寄存器。

然后看not_relocated这个标签。这里是把bss清零。

然后调用cache_on把cache激活，这个是为了提高解压效率。

然后调用wont_overwrite开始解压内核。

内核会解压到ZRELADDR这个地址上。

然后用call_kernel来调用解压后的内核。

然后就是到内核镜像的stext标签这里。arch/arm/kernel/head.S。

先是让cpu进入到svc模式，禁用中断。



在没有激活mmu之前，没法通过虚拟地址访问内存，但是保存处理器信息的区域地址`__proc_info_begin`和`__proc_info_end`是编译内核的时候指定的，且都是虚拟地址。所以就需要把这个虚拟地址转成物理地址才能访问。其实这个很简单，就是一个固定偏移量的问题。



然后是用`__create_page_tables`标签进行页表的创建。







