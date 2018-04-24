---
title: Linux内核启动（一）
date: 2018-03-16 12:06:21
tags:
	- Linux内核
typora-root-url: ..\
---



# uImage的构成

要看uImage的构成，我们就要先看看Makefile的编译过程。

我们把内核的顶层Makefile过一遍。

```
init-y		:= init/
drivers-y	:= drivers/ sound/ firmware/
net-y		:= net/
libs-y		:= lib/
core-y		:= usr/
virt-y		:= virt/
core-y		+= kernel/ certs/ mm/ fs/ ipc/ security/ crypto/ block/

all: vmlinux

vmlinux: scripts/link-vmlinux.sh $(vmlinux-deps) FORCE

$(vmlinux-dirs): prepare scripts
	$(Q)$(MAKE) $(build)=$@ 就这里进入到各个子目录里去编译了。
	
```

vmlinux-dirs对应。

```
init usr arch/arm/kernel arch/arm/mm arch/arm/common arch/arm/probes arch/arm/net arch/arm/crypto arch/arm/firmware arch/arm/mach-s3c24xx arch/arm/plat-samsung kernel certs mm fs ipc security crypto block drivers sound firmware net arch/arm/lib lib virt 
```



uImage的主要部分是vmlinux压缩过的内容。vmlinux是一个elf文件。

看对应的链接脚本。链接脚本有2个，一个链接得到vmlinux，一个链接得到

```
./kernel/vmlinux.lds
./boot/compressed/vmlinux.lds  这个是自动生成的。
```



所以最前面的部分就是指定section为head的代码。

```
 . = 0xC0000000 + 0x00008000;
 .head.text : {
  _text = .;
  *(.head.text)
 }
```

有哪些 代码被指定为head了呢？

```
./include/linux/init.h:103:#define __HEAD               .section        ".head.text","ax"
```

```
./kernel/head.S:79:     __HEAD
./kernel/head.S:505:    __HEAD
./kernel/head.S:606:    __HEAD
./kernel/head-common.S:34:      __HEAD
```



vmlinux，先是objcopy得到二进制的Image，然后得到放在compressed目录下vmlinux。然后是objcopy得到zImage。vmlinx是不压缩的。vmlinuz才是压缩的。

```
$(obj)/Image: vmlinux FORCE
	$(call if_changed,objcopy)
	@$(kecho) '  Kernel: $@ is ready'

$(obj)/compressed/vmlinux: $(obj)/Image FORCE
	$(Q)$(MAKE) $(build)=$(obj)/compressed $@

$(obj)/zImage:	$(obj)/compressed/vmlinux FORCE
	$(call if_changed,objcopy)
	@$(kecho) '  Kernel: $@ is ready'
```

用make V=1来编译，看到最后的步骤是：

```
make -f ./scripts/Makefile.build obj=arch/arm/boot MACHINE=arch/arm/mach-s3c24xx/ arch/arm/boot/Image
make -f ./scripts/Makefile.build obj=arch/arm/boot MACHINE=arch/arm/mach-s3c24xx/ arch/arm/boot/zImage
make -f ./scripts/Makefile.build obj=arch/arm/boot/compressed arch/arm/boot/compressed/vmlinux
make -f ./scripts/Makefile.build obj=arch/arm/boot MACHINE=arch/arm/mach-s3c24xx/ arch/arm/boot/uImage
make -f ./scripts/Makefile.build obj=arch/arm/boot/compressed arch/arm/boot/compressed/vmlinux
```

不过你用uboot的mkimage的时候，可以指定压缩还是不压缩。用-C参数呢。



在调用start_kernel之前，必须先对zImage进行解压，完成页目录构建等基本任务。

调用start_kernel之前的过程，大概分为3个阶段：

1、解压zImage的准备工作。

```
1、查询处理器型号，找到对应的执行代码。进行打开、关闭、清理cache等任务。
2、为MMU构建16KB的页目录。
```

2、解压zImage。

3、获得atags。激活mmu，调用start_kernel。



kernel的System.map，可以看到，前面有一部分是在0x0的 位置，从stext开始，才是C0008000这里。

前面的是位置无关的代码。是放在arch/arm/boot/compressed/head.S里的。

后面的是从arch/arm/kernel/head.S里开始 的。

```
00000000 t __vectors_start
0000000c A cpu_arm920_suspend_size
00001000 t __stubs_start
00001004 t vector_rst
00001020 t vector_irq
000010a0 t vector_dabt
00001120 t vector_pabt
000011a0 t vector_und
00001220 t vector_addrexcptn
00001240 t vector_fiq
00001240 T vector_fiq_offset
c0004000 A swapper_pg_dir
c0008000 T _text
c0008000 T stext
c0008058 t __create_page_tables
```





有多个链接过程。

arch/arm/boot/compressed下面也有一个vmlinux.lds脚本。入口指定为start。

```
OUTPUT_ARCH(arm)
ENTRY(_start)
SECTIONS
{
  . = 0;
  _text = .;
```

链接出来的2个东西，如何拼接起来的呢？

在compressed里的head.S会调用这个__enter_kernel

```
__enter_kernel:
		mov	r0, #0			@ must be 0
 ARM(		mov	pc, r4		)	@ call kernel
 M_CLASS(	add	r4, r4, #1	)	@ enter in Thumb mode for M class
 THUMB(		bx	r4		)	@ entry point is always ARM for A/R classes
```

就是这里进入到arch/arm/kernel/head.S里去的。







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

在解压之前，把mmu打开了，是为了提高效率。在调用call_kernel之后，就要把mmu先禁用。

到后面linux里在打开。

真正内核的入口是是arch/arm/kernel/head.S里的stext标签。



# 参考资料

1、《ARM Linux内核源码剖析》

2、《深度探索Linux操作系统》