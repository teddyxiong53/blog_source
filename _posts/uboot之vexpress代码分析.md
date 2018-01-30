---
title: uboot之vexpress代码分析
date: 2018-01-30 16:01:01
tags:	
	- uboot

---



现在基于vexpress-a9的板子，把嵌入式相关内容重新梳理一遍。

关于这块板子的介绍，这里有：https://wiki.linaro.org/Boards/Vexpress

我分析的uboot代码是2018年1月的。



# 板子基本情况

1、支持多种方式进行boot。有板载flash、SD卡、兼容flash、nfs。

# 模拟运行

1、配置。

```
make ARCH=arm CROSSS_COMPILE=arm-none-eabi- vexpress_ca9x4_defconfig
```

2、编译。

```
make ARCH=arm CROSSS_COMPILE=arm-none-eabi- -j4
```

现在回要求至少gcc6.0的。但是我的arm-none-eabi-gcc是4.8的，不想升级。

于是把报错的地方，改一下，改成要求4.0以上版本就可以编译。

正常编译通过。

3、运行。

```
qemu-system-arm -M vexpress-a9 -kernel u-boot -nographic 
```

启动正常。

把上面的命令包装一下，使用方便一点。

写一个Makefile，跟u-boot目录放在同一层。

```
.PHONY: uboot boot config
ARCH=arm 
CROSS_COMPILE=arm-none-eabi-
export ARCH CROSS_COMPILE

config:
	cd u-boot; make  vexpress_ca9x4_defconfig; cd -
uboot:
	cd u-boot; make -j4; cd -
boot:
	cd u-boot; qemu-system-arm -M vexpress-a9 -kernel u-boot -nographic 
```



首先的配置文件是include/configs/vexpress_common.h

1、默认是CONFIG_VEXPRESS_ORIGINAL_MEMORY_MAP。这个表示使用的是vexpress的默认的内存布局，相对应的扩展内存布局。二者的内存地址不同。

大概分这么几个bank。

```
#define V2M_PA_CS0		0x40000000
#define V2M_PA_CS1		0x44000000
#define V2M_PA_CS2		0x48000000
#define V2M_PA_CS3		0x4c000000
#define V2M_PA_CS7		0x10000000
```



```
#define V2M_BASE		0x60000000 #内存物理地址起始。
#define CONFIG_SYS_TEXT_BASE	0x60800000
```

看看用途。

```
#define V2M_NOR0		(V2M_PA_CS0)
#define V2M_NOR1		(V2M_PA_CS1)
#define V2M_SRAM		(V2M_PA_CS2)
#define V2M_VIDEO_SRAM		(V2M_PA_CS3 + 0x00000000)
#define V2M_LAN9118		(V2M_PA_CS3 + 0x02000000)
#define V2M_ISP1761		(V2M_PA_CS3 + 0x03000000)
```

CS7的就给了各种寄存器，例如串口、定时器、rtc等等。

这些tag都是使能的。

```
#define CONFIG_CMDLINE_TAG		1	/* enable passing of ATAGs */
#define CONFIG_SETUP_MEMORY_TAGS	1
#define CONFIG_SYS_L2CACHE_OFF		1
#define CONFIG_INITRD_TAG		1
```

```
/* PL011 Serial Configuration */
#define CONFIG_PL011_SERIAL
#define CONFIG_PL011_CLOCK		24000000
```



总是看到PL011串口这个东西，PL011是芯片名字吗？

网上查了下，RTC的是对应PL031，看起来是arm公司推出的标准的名字。

PL011串口就是符合armPL011标准的串口。这样驱动就是标准的，不需要另外去管。

```
#define CONFIG_SYS_LOAD_ADDR		(V2M_BASE + 0x8000)
#define LINUX_BOOT_PARAM_ADDR		(V2M_BASE + 0x2000)

```

支持2块，总共1G的内存。

```
#define CONFIG_NR_DRAM_BANKS		2
#define PHYS_SDRAM_1			(V2M_BASE)	/* SDRAM Bank #1 */
#define PHYS_SDRAM_2			(((unsigned int)V2M_BASE) + \
					((unsigned int)0x20000000))
#define PHYS_SDRAM_1_SIZE		0x20000000	/* 512 MB */
#define PHYS_SDRAM_2_SIZE		0x20000000	/* 512 MB */
```

对应的配置文件是：

./configs/vexpress_ca9x4_defconfig

内容只有几条。



```

```

