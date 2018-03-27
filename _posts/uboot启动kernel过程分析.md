---
title: uboot启动kernel过程分析
date: 2016-12-13 23:14:23
tags:
	- linux
	- uboot
---


在cpu刚刚上电的时候，一般内存控制器都没有初始化，无法在DDR里运行程序。为了初始化cpu及其他外设，使得linux内核可以在DDR中运行，必须要有一个先于内核运行的程序，这个程序就bootloader，uboot是最常见的bootloader。

bootm命令用来将内核镜像加载到内存的指定地址处，如果有需要，可能还需要进行解压，然后再根据os类型和cpu体系的不同，给内核传递不同的启动参数，最后启动内核。
# 1. arm架构处理器对linux内核启动之前的环境有5个要求
1. cpu寄存器设置
```
R0=0。
R1=machine ID。定义在linux/arch/arm/tools/mach-types文件里。
R2=内核启动参数在内存中的起始地址。内核会在启动过程中从这个位置读取参数进行解析。
```
2. cpu模式
```
禁止所有中断
必须为SVC模式
```
3. cache和MMU
```
关闭MMU
指令cache可以开启或者关闭
数据cache必须关闭而且不能包含任何脏数据
```
4. 设备
```
DMA设备应当停止工作
```
5. bootloader需要跳转到内核镜像的第一条指令处


# 2. bootm用到的数据结构分析



```
#uboot > bootm 0x31000000 

NAND read: device 0 offset 0x60000, size 0x500000
 5242880 bytes read: OK
*  kernel: cmdline image address = 0x31000000
## Booting kernel from Legacy Image at 31000000 ...
   Image Name:   Linux-4.4.34
   Created:      2018-03-27   4:09:27 UTC
   Image Type:   ARM Linux Kernel Image (uncompressed)
   Data Size:    3013424 Bytes =  2.9 MB
   Load Address: 30008000
   Entry Point:  30008000
   Verifying Checksum ... OK
   kernel data at 0x31000040, len = 0x002dfb30 (3013424)
disable UDC
   Loading Kernel Image ... OK
OK
   kernel loaded at 0x30008000, end = 0x302e7b30
## No init Ramdisk
   ramdisk start = 0x00000000, ramdisk end = 0x00000000
## Transferring control to Linux (at address 30008000) ...

Starting kernel ...
```

这里有内存搬移。

```
memmove_wd ((void *)load_start,
				   (void *)os_data, os_len, CHUNKSZ);

			load_end = load_start + os_len;
			puts("OK\n");
```



最后。

```
theKernel (0, machid, bd->bi_boot_params);
```



