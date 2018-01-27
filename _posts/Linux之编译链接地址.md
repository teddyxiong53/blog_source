---
title: Linux之编译链接地址
date: 2018-01-27 12:01:22
tags:
	- Linux

---



看arch/arm/kernel/vmlinux.lds文件。

```
. = PAGE_OFFSET + TEXT_OFFSET;
```

我们看这个文件包含了`#include <asm/memory.h>`。我们看`./arch/arm/include/asm/memory.h`里的内容。

```
#define PAGE_OFFSET		UL(CONFIG_PAGE_OFFSET)
```

我们找到内核的.config文件。

```
CONFIG_PAGE_OFFSET=0xC0000000
```

然后我们在arch/arm/Makefile里找到：

```
textofs-y	:= 0x00008000
TEXT_OFFSET := $(textofs-y)
```



我们在arch/arm/boot/Makefile里。

```
ifneq ($(MACHINE),)
include $(MACHINE)/Makefile.boot
endif
```

我现在看的MACHINE是mach-vexpress的。

对应的Makefile.boot里这样写：

```
# Empty file waiting for deletion once Makefile.boot isn't needed any more.
# Patch waits for application at
```

这个文件已经没有作用了。

看arch/arm/kernel/head.S文件。

从这个描述来看，前面预留的0x8000（32K）字节，是需要16K来访初始页表。

其实0x4000是够用的了。但是习惯上给0x8000 。

```
/*
 * swapper_pg_dir is the virtual address of the initial page table.
 * We place the page tables 16K below KERNEL_RAM_VADDR.  Therefore, we must
 * make sure that KERNEL_RAM_VADDR is correctly set.  Currently, we expect
 * the least significant 16 bits to be 0x8000, but we could probably
 * relax this restriction to KERNEL_RAM_VADDR >= PAGE_OFFSET + 0x4000.
 */
#define KERNEL_RAM_VADDR	(PAGE_OFFSET + TEXT_OFFSET)
#if (KERNEL_RAM_VADDR & 0xffff) != 0x8000
#error KERNEL_RAM_VADDR must start at 0xXXXX8000
#endif
```



举个例子，下面的地址只是帮助理解，不是真实地址。

启动过程中，一般是把uboot读取到0x0200 0000处（32M），内核镜像一般10M以下。

内核镜像从0x0000 8000处开始放。还不会覆盖到后面的uboot。

等linux启动后，就可以占用uboot之前的位置了。uboot的使命完成了。

linux启动加载过程中涉及的地址，都是物理地址。还没有涉及虚拟内存的知识。



