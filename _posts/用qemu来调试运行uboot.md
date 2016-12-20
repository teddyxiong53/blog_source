---
title: 用qemu来调试运行uboot
date: 2016-12-19 19:28:32
tags:
	- qemu
	- uboot
---
要修改一些uboot代码来进行调试，但是不想频繁烧录程序到板端，用qemu是很方便的调试手段。
当前qemu都已经安装好了的。下载uboot代码。上github上下载一份最新的就行。
# 1. 编译uboot
```
选择一款模拟的板子，就用vexpress_ca9x4这一款
make ARCH=arm CROSS_COMPILE=arm-linux-eabihf- vexpress_ca9x4_defconfig
编译
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j12
```
vexpress系列是ARM官方推出的开发板，介绍在这里。https://www.arm.com/zh/products/tools/development-boards/versatile-express/index.php
ca9x4表示A9的4核CPU。这里有介绍。http://www.myir-tech.com/product/coretile.htm

在uboot代码目录下得到u-boot.bin文件。

# 2. 运行测试
```
teddy@teddy-ubuntu:~/work/qemu/u-boot-master$ qemu-system-arm -M vexpress-a9 -kernel u-boot -nographic 
U-Boot 2017.01-rc1 (Dec 19 2016 - 19:23:33 +0800)

DRAM:  128 MiB
WARNING: Caches not enabled
Flash: 256 MiB
MMC:   MMC: 0
*** Warning - bad CRC, using default environment

In:    serial
Out:   serial
Err:   serial
Net:   smc911x-0
Hit any key to stop autoboot:  0 
=> 
=> 
```
这样就运行起来了。你改了代码只需要再重新生成u-boot.bin再运行就好了。
从打印来看，这块板子的配置是128M的内存，256M的Nand Flash。




