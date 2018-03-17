---
title: Linux内核启动（一）
date: 2018-03-16 12:06:21
tags:
	- Linux内核
typora-root-url: ..\
---



在调用start_kernel之前，必须先对zImage进行解压，完成页目录构建等基本任务。

调用start_kernel之前的过程，大概分为3个阶段：

1、解压zImage的准备工作。

```
1、查询处理器型号，找到对应的执行代码。进行打开、关闭、清理cache等任务。
2、为MMU构建16KB的页目录。
```

2、解压zImage。

3、获得atags。激活mmu，调用start_kernel。





在arm中，对于4GB的内存，以1MB为基本单位进行管理。

所以要有4096个条目。一个条目是4个字节，所以总共是要4K*4=16K的内存空间。

我们把arch/arm/boot/compressed/head.S里的关键代码摘录解释如下：

```
start:
	...
	mov r7,r1 //保存machine id。
	mov r8, r2 //保存atags指针。
	...
	mrs r2, cpsr //读取cpsr寄存器
	//关闭中断。
	...
    .text
    ...
restart:	adr	r0, LC0
		ldmia	r0, {r1, r2, r3, r6, r10, r11, r12}
		ldr	sp, [r0, #28]
		//这段代码的效果是：
		//LC0 --> R1
		//__bss_start -->r2
		//_end --> r3 ，从__bss_start到_end中间就是bss段了。
		//zreladdr -->r4
		//_start -->r5
		//_got_start -->r6
		//_got_end -->ip
		//user_stack+4096 -->sp
not_relocated:	mov	r0, #0  //这里开始清理bss段了。
1:		str	r0, [r2], #4		@ clear bss
		str	r0, [r2], #4
		str	r0, [r2], #4
		str	r0, [r2], #4
		cmp	r2, r3
		blo	1b

		/*
		 * Did we skip the cache setup earlier?
		 * That is indicated by the LSB in r4.
		 * Do it now if so.
		 */
		tst	r4, #1
		bic	r4, r4, #1
		blne	cache_on //这里打开cache。
		
		...
		bls	wont_overwrite//这里开始解压内核。
		
__setup_mmu:	sub	r3, r4, #16384 //这个被cache_on调用。
		bic	r3, r3, #0xff		
		bic	r3, r3, #0x3f00
```





![Linux启动时内核解压布局](/images/Linux启动时内核解压布局.png)



而页目录的条目情况是这样的：

| Entry | 物理地址        | 虚拟地址                          |
| ----- | ----------- | ----------------------------- |
| 4095  | 0x5000 7ffc | 0xfff0 0c12                   |
| ...   |             |                               |
| 1535  | 0x5000 57fc | 0x5fff0 0c1e                  |
| ...   |             | 对这256项设置cacheable和bufferable。 |
| 1280  | 0x5000 5400 | 0x5000 0c1e                   |
| ...   |             |                               |
| 1     | 0x5000 4004 | 0x0010 0c12                   |
| 0     | 0x5000 4000 | 0x0000 0c12                   |

虚拟地址这边，覆盖的是整个线性地址空间的4G，实际上物理内存就是256M，就是我们要设置cacheable和bufferable的那段地址空间。

这些都是在setup_mmu里完成的。



下面就要开始解压内核了。用的就是wont_overwrite这个标签。



解压完之后，就是建立临时页表，在0x5000 4000这个位置开始，一共占据0x4000字节空间。



# 参考资料

1、《ARM Linux内核源码剖析》