---
title: Linux内核之memblock和bootmem
date: 2018-03-29 22:41:58
tags:
	- Linux内核

---



memblock和bootmem的关系

1、memblock必须有的，bootmem可以没有。

2、配置CONFIG_NO_BOOTMEM，bootmem就会编译到nobootmem.c文件。这个里面的接口实现就是用memblock来实现的。



#memblock

从代码里看，memblock出现的时机比bootmem早。

```
	arm_memblock_init(&meminfo, mdesc);//memblock在这里。
	paging_init(mdesc);//紧接着上面函数，这个里面调用了bootmem的初始化。
```

所以，我们先看memblock的情况。

memblock是在系统启动阶段进行简单的内存管理。记录物理内存的使用情况。

在进一步介绍memblock之前，我们有必要把系统内存的使用情况理一遍。

1、内存中有些部分是永久分配给内核的，包括内核代码段、数据段、ramdisk、fdt。

这部分称为静态内存。

2、gpu、camera都要预留大量连续内存，这部分平时不用，但是必须提前预留好。这个就叫预留内存。

3、其他部分，就是动态内存。



memblock把物理内存划分为几个内存区。具体是几个，由NR_BANKS这个宏来决定，在mx2上，是16个。

```
struct meminfo {
	int nr_banks;
	struct membank bank[NR_BANKS];
};
```



预留内存的代码：

```
memblock_reserve(__pa(_stext), _end - _stext);//内核代码段和数据段。
memblock_reserve(phys_initrd_start, phys_initrd_size);//initrd
arm_mm_memblock_reserve();
	memblock_reserve(__pa(swapper_pg_dir), PTRS_PER_PGD * sizeof(pgd_t));//页表区域。
arm_dt_memblock_reserve();
```

最后打印出来看的。

memblock就分为memory和reserved这2个部分。

```
memblock_dump(&memblock.memory, "memory");
memblock_dump(&memblock.reserved, "reserved");
```

不过默认是不会打印出来的，你在bootargs里加上：

```
memblock=debug
```

就好了。

这个是根据代码里的推断出来的。

```
static int __init early_memblock(char *p)
{
	if (p && strstr(p, "debug"))
		memblock_debug = 1;
	return 0;
}
early_param("memblock", early_memblock);
```



```
memblock_reserve: [0x60100000-0x60a96fb3] arm_memblock_init+0x24/0x6c
memblock_reserve: [0x60004000-0x60007fff] arm_mm_memblock_reserve+0x18/0x1c
memblock_reserve: [0x64000000-0x6400c149] early_init_dt_reserve_memory_arch+0x18/0x1c
MEMBLOCK configuration:
 memory size = 0x08000000 reserved size = 0x009a70fe
 memory.cnt  = 0x1
 memory[0x0]    [0x60000000-0x67ffffff], 0x08000000 bytes flags: 0x0
 reserved.cnt  = 0x3
 reserved[0x0]  [0x60004000-0x60007fff], 0x00004000 bytes flags: 0x0
 reserved[0x1]  [0x60100000-0x60a96fb3], 0x00996fb4 bytes flags: 0x0
 reserved[0x2]  [0x64000000-0x6400c149], 0x0000c14a bytes flags: 0x0
memblock_reserve: [0x67ffe000-0x67ffffff] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ffd000-0x67ffdfff] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ffcfd8-0x67ffcfff] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ffb000-0x67ffbfff] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ffa000-0x67ffafff] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ff9000-0x67ff9fff] memblock_alloc_range_nid+0x44/0x5c
memblock_virt_alloc_try_nid_nopanic: 1048576 bytes align=0x0 nid=0 from=0x0 max_addr=0x0 alloc_node_mem_map+0x68/0xc0
memblock_reserve: [0x67ef9000-0x67ff8fff] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid_nopanic: 16 bytes align=0x0 nid=0 from=0x0 max_addr=0x0 free_area_init_node+0x2d8/0x334
memblock_reserve: [0x67ffcfc0-0x67ffcfcf] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 32 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 setup_arch+0x814/0xb8c
memblock_reserve: [0x67ffcf80-0x67ffcf9f] memblock_virt_alloc_internal+0xec/0x1cc
memblock_reserve: [0x67eee43c-0x67ef8fff] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ffcfa4-0x67ffcfbe] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ffcf64-0x67ffcf7e] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ffcf48-0x67ffcf62] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ffcf2c-0x67ffcf46] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ffcf14-0x67ffcf2b] memblock_alloc_range_nid+0x44/0x5c
memblock_reserve: [0x67ffcefc-0x67ffcf13] memblock_alloc_range_nid+0x44/0x5c
CPU: All CPU(s) started in SVC mode.
random: fast init done
memblock_virt_alloc_try_nid: 78 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 start_kernel+0xa4/0x36c
memblock_reserve: [0x67ffce80-0x67ffcecd] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 78 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 start_kernel+0xd0/0x36c
memblock_reserve: [0x67ffce00-0x67ffce4d] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 78 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 start_kernel+0xf4/0x36c
memblock_reserve: [0x67ffcd80-0x67ffcdcd] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid_nopanic: 4096 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_alloc_alloc_info+0x4c/0x94
memblock_reserve: [0x67eed400-0x67eee3ff] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid_nopanic: 4096 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_embed_first_chunk+0x488/0x728
memblock_reserve: [0x67eec400-0x67eed3ff] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid_nopanic: 262144 bytes align=0x1000 nid=-1 from=0xdfffffff max_addr=0x0 pcpu_dfl_fc_alloc+0x24/0x2c
memblock_reserve: [0x67eac000-0x67eebfff] memblock_virt_alloc_internal+0xec/0x1cc
__memblock_free_early: [0x00000067ebc000-0x00000067ebbfff] pcpu_dfl_fc_free+0xc/0x10
__memblock_free_early: [0x00000067ecc000-0x00000067ecbfff] pcpu_dfl_fc_free+0xc/0x10
__memblock_free_early: [0x00000067edc000-0x00000067edbfff] pcpu_dfl_fc_free+0xc/0x10
__memblock_free_early: [0x00000067eec000-0x00000067eebfff] pcpu_dfl_fc_free+0xc/0x10
percpu: Embedded 16 pages/cpu @87eac000 s36428 r8192 d20916 u65536
memblock_virt_alloc_try_nid: 4 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_setup_first_chunk+0x3d4/0x998
memblock_reserve: [0x67ffcd40-0x67ffcd43] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 4 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_setup_first_chunk+0x3f4/0x998
memblock_reserve: [0x67ffcd00-0x67ffcd03] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 16 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_setup_first_chunk+0x41c/0x998
memblock_reserve: [0x67ffccc0-0x67ffcccf] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 16 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_setup_first_chunk+0x43c/0x998
memblock_reserve: [0x67ffcc80-0x67ffcc8f] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 128 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_setup_first_chunk+0x84c/0x998
memblock_reserve: [0x67ffcc00-0x67ffcc7f] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 69 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_alloc_first_chunk+0x60/0x278
memblock_reserve: [0x67ffcb80-0x67ffcbc4] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 384 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_alloc_first_chunk+0xa4/0x278
memblock_reserve: [0x67ffca00-0x67ffcb7f] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 388 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_alloc_first_chunk+0xc4/0x278
memblock_reserve: [0x67ffc840-0x67ffc9c3] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 60 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_alloc_first_chunk+0xec/0x278
memblock_reserve: [0x67ffc800-0x67ffc83b] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 69 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_alloc_first_chunk+0x60/0x278
memblock_reserve: [0x67ffc780-0x67ffc7c4] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 768 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_alloc_first_chunk+0xa4/0x278
memblock_reserve: [0x67ffc480-0x67ffc77f] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 772 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_alloc_first_chunk+0xc4/0x278
memblock_reserve: [0x67ffc140-0x67ffc443] memblock_virt_alloc_internal+0xec/0x1cc
memblock_virt_alloc_try_nid: 120 bytes align=0x0 nid=-1 from=0x0 max_addr=0x0 pcpu_alloc_first_chunk+0xec/0x278
memblock_reserve: [0x67ffc0c0-0x67ffc137] memblock_virt_alloc_internal+0xec/0x1cc
__memblock_free_early: [0x00000067eed400-0x00000067eee3ff] pcpu_free_alloc_info+0x14/0x18
__memblock_free_early: [0x00000067eec400-0x00000067eed3ff] pcpu_embed_first_chunk+0x714/0x728
Built 1 zonelists, mobility grouping on.  Total pages: 32512
```



内核如何探测物理内存的拓扑结构呢？

通过DDR的模式寄存器，可以获得内存密度，进而推算出内存容量。

这部分工作是由uboot完成，通过atag传递给内核。



# bootmem





# 参考资料

1、内核早期内存分配器 - memblock与bootmem

https://blog.csdn.net/modianwutong/article/details/53162142