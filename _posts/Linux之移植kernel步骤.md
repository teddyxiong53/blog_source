---
title: Linux之移植kernel步骤
date: 2017-08-15 23:18:26
tags:
	- Linux
---



以tq2440的为例进行说明。

1、下载内核源代码。

2、配置ARCH和CROSS_COMPILE。

3、修改时钟。因为tq2440的时钟是12M的。在arch/arm/mach-s3c2440/mach-smdk2440.c。

```
s3c24xx_init_clocks(16934400);改为12*1000*1000;
```

4、做tq2440的.config文件。

采用拷贝2410的defconfg文件，然后进行menuconfig。

加入一些个人配置信息，保存配置文件。

5、修改机器码。

tq2440的uboot里配置了机器码为168，所以内核也要改成这个，否则就启动不了。

在arch/arm/tools/mach-types里，

```
s3c2440			ARCH_S3C2440		S3C2440			362
```

把362改成168 。

6、现在编译。

```
make zImage
```

7、nand flash驱动修改。

在arch/arm/plat-s3c24xx/common-smdk.c里。

```
static struct mtd_partition smdk_default_nand_part[] = {
```

这个结构体的内容根据实际情况改一下大小，位置等。

8、然后把nand flash在menuconfig里选上，重新编译。

9、编译busybox。

10、网卡驱动修改。

内核里的网卡驱动不适合tq2440的DM9000E这颗芯片。所以需要修改drivers/net/dm9000.c文件。

11、lcd驱动修改。

在drivers/video/s3c2410fb.c里修改。

12、led驱动修改。

内核里已经带了led驱动了，在drivers/led/leds-s3c24xx.c里。

另外arch/arm/plat-s3c24xx/common-smdk.c里有配置led。

我把common-smdk.c里的led代码注释掉。

然后我们在smdk_machine_init里修改一下代码，让led都亮起来。

我们自己用char dev写一个led 驱动。

13、中断方式的按键驱动。

也是普通的char dev。

14、写pwm驱动。驱动蜂鸣器。





