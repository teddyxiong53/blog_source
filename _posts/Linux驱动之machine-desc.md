---
title: Linux驱动之machine desc
date: 2018-03-01 10:22:19
tags:
	- Linux驱动

---



machine_desc结构体在内核移植过程中很重要。内核通过machine_desc结构体来控制系统体系架构部分的初始化。

结构体定义如下：arch/arm/include/asm/mach/arch.h

```
struct machine_desc {
  unsigned int nr;//这个就是uboot传递过来的机器码。
  uint phys_io;//物理io的起始
  uint io_pg_offst;// io page table偏移
  char *name ;
  unsigned long boot_params;//tag list，设置在ram addr + 0x100的位置。
  uint video_start;// video ram 
  uint video_end;
  uint reserve_lp0:1;
  //lp1/lp2:1
  uint soft_reboot:1;
  void (*fixup)(struct machine_desc* ...);
  void (*map_io)();
  void (*init_irq)();
  struct sys_timer *timer;
  void (*init_machine)();
};
```

这个结构体通过MACHINE_START宏来进行初始化。调用是被setup_machine调用到的。

```
setup_arch
	setup_machine
	
```

MACHINE_START定义了machine_desc结构体放在`(__section__(".arch.info.init"))`。

这个位置的内存在内核起来后会被释放掉的。







#map-base.h作用

当我们开启了mmu之后，使用的都是虚拟地址，这时就要考虑pa到va的映射问题。

建立映射表的3个关键部分是：

1、映射表。

```
1、映射表是具体的pa和va的起始地址定义。
我们指定了虚拟地址的基地址，就是S3C_ADDR_BASE 0xFD00 0000
在我们开启了mmu之后，其映射的虚拟地址都是根据这个S3C_ADDR_BASE加offset来得到某个具体的reg的。
这样我们就可以通过va来操作reg了。
映射表一般都是在arch/arm/xxx/map_xx.h里定义。
```



2、映射表建立函数。

3、映射表建立函数被调用。



#iotable_init

```
#define S3C24XX_VA_IRQ      S3C_VA_IRQ   #define S3C24XX_VA_MEMCTRL  S3C_VA_MEM   #define S3C24XX_VA_UART     S3C_VA_UART      #define S3C24XX_VA_TIMER    S3C_VA_TIMER   #define S3C24XX_VA_CLKPWR   S3C_VA_SYS   #define S3C24XX_VA_WATCHDOG S3C_VA_WATCHDOG
```



我尝试发现这些地址映射的规律，但发现无明显的规律，基本是映射到“一个段"。事实上也是任意的，但其地址都是在vmalloc地址区域的末端。