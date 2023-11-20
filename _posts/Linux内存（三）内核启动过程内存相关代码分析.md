---
title: Linux内存（三）内核启动过程内存相关代码分析
date: 2018-03-19 13:51:49
tags:
	- Linux

---

--

# 1

## 1

### 汇编里的我先不管，从start_kernel看起。

第一个相关的是setup_arch函数里。

给init_mm这个全局变量赋值了。

```
init_mm.start_code = (unsigned long) _text;
init_mm.end_code   = (unsigned long) _etext;
init_mm.end_data   = (unsigned long) _edata;
init_mm.brk	   = (unsigned long) _end;
```

然后是固定映射。

```
early_fixmap_init();
early_ioremap_init();
```

early_fixmap_init里。

```
开始涉及到pmd了。
pmd = fixmap_pmd(FIXADDR_TOP);
FIXADDR_TOP这个地址是 0xfff0 0000 - 4K。
fixmap_pmd的实现如下。
static inline pmd_t * __init fixmap_pmd(unsigned long addr)
{
	pgd_t *pgd = pgd_offset_k(addr);
	pud_t *pud = pud_offset(pgd, addr);
	pmd_t *pmd = pmd_offset(pud, addr);

	return pmd;
}
开始涉及pgd、pud、pmd。
pgd_offset(&init_mm, 0xFFEFF000)

init_mm->pgd + 0xFFEFF000>>21 //除以2M。
init_mm->pgd + 0x7ff

而定义的时候，init_mm的pgd就赋值了。
struct mm_struct init_mm = {
	.mm_rb		= RB_ROOT,
	.pgd		= swapper_pg_dir,//是一个宏，是0
所以fixmap_pmd得到的内部情况是这样的：
pgd = 0x7ff
pud = 0x7ff
pmd = 0x7ff

然后是调用pmd_populate_kernel
第一次产生的是
pmdp[0]:6095a811, pmdp[1]:6095ac11

```

### early_mm_init

调用了这2个函数。

```
build_mem_type_table();
early_paging_init(mdesc);
```

build_mem_type_table

```
这个条件满足。
(cpu_arch >= CPU_ARCH_ARMv6 && (cr & CR_XP))
这个满足。
if (cpu_arch >= CPU_ARCH_ARMv7 && (cr & CR_TRE))
得到的memory  policy是：
Memory policy: Data cache writeback

```

early_paging_init

这个函数直接返回的。

### adjust_lowmem_bounds

从名字上看，是调整低端内存边界。

```
static void * __initdata vmalloc_min =
	(void *)(VMALLOC_END - (240 << 20) - VMALLOC_OFFSET);
    算出来就是：
    0xff800000 - 0x0f000000 - 0x800000 = 0xf0000000
    我加打印得到是：
    xhl -- func:adjust_lowmem_bounds, line:1187, vmalloc_limit:80000000,vmalloc_min:d0000000,PAGE_OFFSET:00000000, PHYS_OFFSET:f0000000
    
    xhl -- func:adjust_lowmem_bounds, line:1253 ,arm_lowmem_limit:68000000, high_memory:88000000,memblock_limit:68000000
```

### arm_memblock_init

```
1、保留kernel占据那部分内存。
memblock_reserve(__pa(KERNEL_START), KERNEL_END - KERNEL_START);
2、保留initrd要的内存。
3、保留pgd要的内存。
arm_mm_memblock_reserve、
4、fdt的内存保留。
5、dma的保留。
6、打印当前的情况。
```

adjust_lowmem_bounds 会被再调用一次。

### paging_init

这里是最重要的部分了。

里面调用的函数单独列，因为都挺复杂的。

### prepare_page_table

这里就是把pmd数据清零一下。

pmd数据分为

1、ko文件占据空间部分。就是0x8000 0000下面的16M。

2、0到PAGE_OFFSET部分。就是0 到0x8000 0000这部分。

3、内核空间的低端内存部分。

### map_lowmem

从名字上看，是映射低端内存。

里面中断是create_mapping函数调用。

里面就是alloc pgd、pmd这些空间。



#### mm_init

这个函数也是一个重要函数。里面调用了多个函数。

CONFIG_NO_BOOTMEM=y

我的系统默认是选择没有bootmem的。

mem_init。

```

```

