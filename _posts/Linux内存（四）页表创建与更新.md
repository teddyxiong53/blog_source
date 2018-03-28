---
title: Linux内存（四）页表创建与更新
date: 2018-03-28 16:12:53
tags:
	- Linux内存

---



简单来说，讨论Linux页表就是讨论进程的页表。这句话的意思是，页表的创建和更新都包含在进程的创建和更新中。

Linux内核采用的是写时复制的技术。

当创建一个新的进程的时候，子进程会完全复制父进程的页表。父进程和子进程都把页表设置为写保护，这样父进程和子进程无论谁进行写操作，都会导致缺页异常，就把不同的部分分配新的页。主要随着时间推移，父进程和子进程的页表就越来越不同了。

所以，讨论第一个进程的页表的情况，可以看出页表的相关情况了。

第一个进程的init_task，对应的页表是init_mm的初始化页表swapper_pg_dir。

```
struct mm_struct init_mm = {
	.mm_rb		= RB_ROOT,
	.pgd		= swapper_pg_dir,
```



在arch/arm/kernel/head.S里，

```
/*
 * swapper_pg_dir is the virtual address of the initial page table.
 * We place the page tables 16K below KERNEL_RAM_VADDR.  Therefore, we must
 * make sure that KERNEL_RAM_VADDR is correctly set.  Currently, we expect
 * the least significant 16 bits to be 0x8000, but we could probably
 * relax this restriction to KERNEL_RAM_VADDR >= PAGE_OFFSET + 0x4000.
 */
 意思是说，swapper_pg_dir是初始化页表的虚拟地址。
 我们把这个放在KERNEL_RAM_VADDR这里。
 因此，我们必须保证KERNEL_RAM_VADDR的值正确设置。
 
```

```
#define KERNEL_RAM_VADDR	(PAGE_OFFSET + TEXT_OFFSET)
#if (KERNEL_RAM_VADDR & 0xffff) != 0x8000
#error KERNEL_RAM_VADDR must start at 0xXXXX8000
#endif
```

TEXT_OFFSET是0x8000 。而且要求是这样的。

```
extern pgd_t swapper_pg_dir[PTRS_PER_PGD];//PTRS_PER_PGD = 2048
```

看System.map内容。

```
00001240 t vector_fiq
00001240 T vector_fiq_offset
c0004000 A swapper_pg_dir
c0008000 T _text
c0008000 T stext
c0008058 t __create_page_tables
```

初始化页表的都是无效地址。

然后创建进程时，调用

```
do_fork
	copy_process
		copy_mm
			dup_mm
				dup_mmap
					copy_page_range，这个函数就是负责页表的拷贝。
						copy_pud_range
							copy_pmd_range
								copy_pte_range
```





# 参考资料

1、linux页表创建与更新

https://blog.csdn.net/evenness/article/details/7656812