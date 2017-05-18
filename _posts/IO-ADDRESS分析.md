---
title: IO_ADDRESS分析
date: 2017-05-18 18:49:18
tags:

	- Linux驱动

---

Linux驱动编程里，需要访问soc的寄存器，如何才能操作到寄存器呢？

Linux提供了两种机制，一种是动态映射ioremap，一种是静态映射map_desc。IO_ADDRESS就是在静态映射方式时使用的。

ioremap是简单一些，用得也多，我们先看ioremap。

这个函数的情况是这样：

```
arch/arm/include/asm/io.h里
#define ioremap(cookie,size)		__arm_ioremap(cookie, size, MT_DEVICE)
__arm_ioremap在arch/arm/mm/ioremap.c里。
其实现就在这个文件里。

```

我们把物理地址映射到虚拟地址后，就可以通过虚拟地址来直接操作寄存器了，跟直接操作物理地址是一样的效果。

注意：ioremap的大小是以页为单位的。也就是4KB。

下面看静态映射。

在将Linux移植到目标电路板上时，通常会建立外设IO内存物理地址到虚拟地址的静态映射，具体操作方式就是在电路板对应的map_desc结构体数组里添加新的成员。这个是内核移植过程中重要的一步。

以S3C2440的为例，在arch/arm/mach-smdk2440.c里。

定义了static struct map_desc smdk2440_iodesc。

静态映射要获取虚拟地址，就要用到IO_ADDRESS来获取了。

假设板上有个SRAM，其物理地址为0x30000000。我们现在通过静态映射的方式来使用它。

```
static void sram_test()
{
	void *sram_p;
	char str[] = "hello, sram \n";
	sram_p = (void *)IO_ADDRESS(SRAM_BASE);
	memcpy(sram_p, str, sizeof(str));
	printk(sram_p);
	
}
static __init int sram_init()
{
	struct resource *res;
	res = request_mem_region(SRAM_BASE, SRAM_SIZE, "sram region");
	sram_test();
}

static __exit void sram_exit()
{
	release_mem_region(SRAM_BASE, SRAM_SIZE);
	
}
```





