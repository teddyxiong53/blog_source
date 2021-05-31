---
title: Linux内核之mtd（一）
date: 2018-04-06 21:57:38
tags:
	- Linux内核

---

--

有两个流行的用户模块可启用对闪存的访问： 

MTD_CHAR 和 MTD_BLOCK 。

MTD_CHAR 提供对闪存的原始字符访问，

而 MTD_BLOCK 将闪存设计为可以在上面创建文件系统的常规块设备（象 IDE 磁盘）。



与 MTD_CHAR 关联的设备是 /dev/mtd0、mtd1、mtd2（等等），而与 MTD_BLOCK 关联的设备是 /dev/mtdblock0、mtdblock1（等等）。

由于 MTD_BLOCK 设备提供象块设备那样的模拟，通常更可取的是在这个模拟基础上创建象 FTL 和 JFFS2 那样的文件系统。



# 什么是mtd

mtd的Memory Technology Device的缩写。是内存技术设备。

是用来实现对flash的抽象的。

mtd是用于访问memory设备的Linux子系统。

memory设备包括：ram、rom、flash。

mtd的设计目的：

让新的memory驱动更加简单。

做法是：

在硬件和上层之间，加了一层抽象层。

传统意义上，unix系统只认识块设备和字符设备。

flash既不满足块设备描述，也不满足字符设备描述。

它表现类似于块设备，又有所不同。

例如，块设备不区分erase和write操作。



有了mtd，驱动工程师就不用关心块设备和字符设备这些事情了。只要专注把硬件相关的内容写好就行。

mtd是一个中间层，下面是flash驱动，上面是文件系统。

```
------------------------
设备节点
------------------------
mtd字符设备   mtd块设备
------------------------
mtd原始设备
------------------------
flash驱动 （驱动工程师关注这个就可以了）
------------------------
```

```
#define MTD_CHAR_MAJOR 90
#define MTD_BLOCK_MAJOR 31
```



# mtd跟下面的接口

mtd下面是具体的flash芯片。

mtd怎么跟flash 打交道呢？

一个重要结构体就是mtd_info。定义在linux/mtd/mtd.h里。mtd目录下的头文件还不少。有38个。

```
1. uchar type // MTD_RAM/ROM/NORFLASH/NANDFLASH
2. u32 flags // MTD_WRITEABLE ...
3. u64 size 
4. u32 erasesize
5. u32 writesize
6. u32 writebufsize
7. u32 oobsize
8. u32 oobavail
9. uint erasesize_shift
10. uinit writesize_shift
11. uint bitflip_threshold
12. char *name
13. int index
14. struct nand_ecclayout *ecclayout
15. uint ecc_step_size
16. uint ecc_strength
17. int numeraseregions
18. struct mtd_erase_region_info *eraseregions
19. int (*_erase)(...)
20. _point
21. _unpoint
22. _get_unmapped_area
23. _read
24. _write
25. _panic_write
26. _read_oob
27. _write_oob
28. _get_fact_prot_info
29. _read_fact_prot_reg
...
30. struct backing_dev_info *backing_dev_info
31. struct notifier_block reboot_notifier
32. struct mtd_ecc_stats ecc_stats
33. int subpage_sft
34. void *priv
35. struct module *owner
36. struct device dev
37. int usecount
```

mtd_partition结构体用来描述flash上的一个分区。

```
1. char *name
2. u64 size
3. u64 offset
4. u32 mask_flags
5. struct nand_ecclayout *ecclayout
```



# nor flash驱动

linux里，实现了针对CFI（公共Flash接口）、JEDEC这些接口的通用nor flash驱动。

nor flash驱动需要做的工作不多。

内核自带的nor flash驱动在drivers/mtd/maps/physmap.c。编译得到physmap.ko文件。

insmod后，会在/dev目录下生成对应的节点。

我们先看看这个文件。



注册一个块设备，需要这些步骤：

1、分配mtd_info结构体和map_info结构体。

2、设置这2个结构体。

3、add_mtd_partitions创建块设备，add_mtd_device创建字符设备。

一个简单的例子就是这样的。

```
struct mtd_info *xx_nor_mtd_info;
struct map_info *xx_nor_map_info;

struct mtd_partition xx_nor_partitions[] = {
    [0] = {
        .name = "boot",
        .size = 0x40000,
        .offset = 0,
    },
    [1] = {
        .name = "kernel",
        .offset = MTDPART_OFS_APPEND,
        .size= MTDPART_SIZ_FULL,
    },
};

char *xx_nor_types[] = {"cfi_probe", "jedec_probe", NULL};

static int xx_nor_init()
{
    int ret;
    xx_nor_mtd_info = kzalloc(sizeof(struct mtd_info), GFP_KERNEL);
    xx_nor_map_info = kzalloc(sizeof(struct map_info), GFP_KERNEL);

    xx_nor_map_info->name = "xx_nor";
    xx_nor_map_info->phys = 0; //物理地址
    xx_nor_map_info->size= 0x1000000;//大于等于实际物理地址
    xx_nor_map_info->bankwidth = 2;// 16bit 位宽
    xx_nor_map_info->virt = ioremap(0x0, xx_nor_map_info->size);//拿到虚拟地址
    simple_map_init(xx_nor_map_info);

    xx_nor_mtd_info = do_map_probe("cfi_probe", xx_nor_types);
    if(!xx_nor_mtd_info) {
        do_map_probe("jedec_probe", xx_nor_types);
    }
    if(!xx_nor_mtd_info) {
        printk("flash not ok\n");
        goto err;
    }
    xx_nor_mtd_info->owner = THIS_MODULE;
    add_mtd_partitions(xx_nor_mtd_info, xx_nor_partitions, 2);
    return 0;
err:
    iounmap(xx_nor_map_info->virt);
    kfree(xx_nor_map_info);
    kfree(xx_nor_mtd_info);
    return -1;
}
```

对于mini2440，因为nor flash直接接到了CPU的内存空间上，因此是可以直接使用通用的drivers/mtd/maps/physmap.c文件。

只需要配置MTD_PHYSMAP。

我们只需要在bsp文件里，增加一个平台设备，名字跟physmap.c里的 “physmap-flash”这个名字一样就好了。

```
struct platform_device ldd6410_device_nor = {
  .name = "physmap-flash", 
  .id = 0,
  .dev = {
    .platform_data = &ldd6410_flash_data,
  },
  .num_resources = 1,
  .resource = &ldd6410_nor_resource,
};
```

而对于三星平台的，nand驱动也是有的了。你只需要再bsp里增加对应的平台设备就好了。







# 参考资料

1、25.Linux-Nor Flash驱动(详解)

https://www.cnblogs.com/lifexy/p/7737174.html

2、linux内核中mtd架构分析

https://www.cnblogs.com/embedded-linux/p/5816970.html

3、什么是MTD分区和NAND flash?

https://www.cnblogs.com/hnrainll/archive/2011/05/17/2048288.html