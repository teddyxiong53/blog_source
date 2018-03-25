---
title: qemu之mini2440环境搭建（三）
date: 2018-03-25 11:20:12
tags:
	- qemu

---



终于把这个环境搭建好了。现在依据这个版本来深入学习linux源代码。

我首先要做的就是I2C的实验。

不过当前还是遗留了一个问题，就是我的kernel版本是4.4的。

我还是换回2.6.35的，看看是否可以运行。

这个还是启动的时候会卡住。

其实我主要是觉得4.4的有设备树，读代码不直观。

现在看看哪个版本开始引入的设备树。

https://www.quora.com/Which-version-of-Linux-Kernel-introduced-the-device-tree-support

从这篇文章看，3.7版本后，arm架构下的设备树才变得普遍。

```
Kernel 3.7 onwards DT architecture became common in arm while PPC architecute adopted DT as early as 2.6.22
```

这篇文章描述了3.x的版本区别。

https://www.baidu.com/link?url=6bKHeX46n4auq5-7iNJ-2ehO42lpiUrM3t01Z-hTHk6BQzf2eOr0kCISRgA7PWdD7-5b45y1wTyXSneRfmmWdfT3ttokJTR8qjJggcStdOO&wd=&eqid=c00849ab0001af55000000035ab7185b

我选择3.10的看看。

https://mirrors.edge.kernel.org/pub/linux/kernel/v3.0/

从这里下载代码。

我仔细看了一下4.4 里面的mini2440的代码，没有使用设备树的特性。所以可以用4.4的来其实。

好吧。还是在4.4的基础上看。



我的一个疑问是：我分给rootfs的区域没有这么大，这里为什么显示这么大呢？

```
/ # df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root                58.6M     11.2M     47.4M  19% /
/ # 
```

我的本意是给rootfs 16M的空间的。

查看proc信息。

这个3aa 0000是怎么来的？我并没有把剩余的都给它啊。

```
/proc # cat mtd 
dev:    size   erasesize  name
mtd0: 00040000 00004000 "u-boot"
mtd1: 00020000 00004000 "u-boot-env"
mtd2: 00500000 00004000 "kernel"
mtd3: 03aa0000 00004000 "root"
```

现在要去看看flashimg做了些什么。

oob的是跟page size关联的。page size确定了，oob也就确定了。

```
struct ecc_info const ecc_tab[] = {
	{
	.page_size = 256,
	.oob_size = 8,
	.ecc_nb = 3,
	.ecc_pos = { 0, 1, 2 },
	},

	{
	.page_size = 512,
	.oob_size = 16,
	.ecc_nb = 6,
	.ecc_pos = { 0, 1, 2, 3, 6, 7 },
	},
```

flashimg的整个过程就是读取文件，拼接到一起，拼接的过程怎么处理oob，这里是关键。

我单步调试一下flashimg程序。

```
teddy@teddy-ubuntu:~/work/mini2440-lab$ make nand
Makefile:49: warning: overriding recipe for target 'uboot'
Makefile:32: warning: ignoring old recipe for target 'uboot'
cd ./image ;flashimg -s 64M -t nand -f nand.bin -p uboot.part -w boot,u-boot.bin -w kernel,uImage -w root,rootfs.jffs2 -z 512 ;cd -
size img = 67108864
Partition list:
name    offset          size
boot    0x00000000      0x00100000
kernel  0x00060000      0x00500000
root    0x00560000      0x01000000
Flash type: NAND
Read content file

Partition boot found (0x100000 bytes @0x0)
off real=0
  st_size=234120 part_len=1081344
Erase partition
Write partition:
Write 457 blocks at 0

Partition kernel found (0x500000 bytes @0x60000)
off real=63000
  st_size=3014040 part_len=5406720
Erase partition
Write partition:
Write 5886 blocks at 393216

Partition root found (0x1000000 bytes @0x560000)
off real=58b000
  st_size=10110304 part_len=17301504
Erase partition
Write partition:
Write 19746 blocks at 5636096
/home/teddy/work/mini2440-lab
```

这个过程我觉得是没有问题的。

那就看mkfs.jffs2的时候。

或者，你既然是要3aa 0000这么长。我就给你这么长看看。

```
>>> 0x3aa0000+0x560000
67108864
>>> hex(67108864)
'0x4000000'
```

这个就是把剩下的都给了rootfs了。

不过这样制作出来的nand.bin，启动后，仍然会打印很多的nand相关的打印。

给的尺寸越大，打印越久。

感觉像是在检测所有的内容一样。

```
------------[ cut here ]------------
WARNING: CPU: 0 PID: 800 at drivers/mtd/nand/nand_base.c:934 nand_wait+0x110/0x138()
Modules linked in:
CPU: 0 PID: 800 Comm: jffs2_gcd_mtd3 Tainted: G        W       4.4.34 #2
Hardware name: MINI2440
[<c000f608>] (unwind_backtrace) from [<c000d250>] (show_stack+0x10/0x14)
[<c000d250>] (show_stack) from [<c001751c>] (warn_slowpath_common+0x74/0xac)
[<c001751c>] (warn_slowpath_common) from [<c00175f0>] (warn_slowpath_null+0x1c/0x24)
[<c00175f0>] (warn_slowpath_null) from [<c028d7cc>] (nand_wait+0x110/0x138)
[<c028d7cc>] (nand_wait) from [<c0289910>] (nand_write_oob_std+0x64/0x70)
[<c0289910>] (nand_write_oob_std) from [<c028ae84>] (nand_do_write_oob+0x1b4/0x218)
[<c028ae84>] (nand_do_write_oob) from [<c028bd38>] (nand_write_oob+0xa4/0xb8)
[<c028bd38>] (nand_write_oob) from [<c01a26b0>] (jffs2_write_nand_cleanmarker+0x98/0xe8)
[<c01a26b0>] (jffs2_write_nand_cleanmarker) from [<c019ee4c>] (jffs2_erase_pending_blocks+0x548/0x69c)
[<c019ee4c>] (jffs2_erase_pending_blocks) from [<c019d900>] (jffs2_garbage_collect_pass+0x1a0/0x668)
[<c019d900>] (jffs2_garbage_collect_pass) from [<c019f07c>] (jffs2_garbage_collect_thread+0xdc/0x1d8)
[<c019f07c>] (jffs2_garbage_collect_thread) from [<c002ef54>] (kthread+0xc0/0xdc)
[<c002ef54>] (kthread) from [<c000a490>] (ret_from_fork+0x14/0x24)
---[ end trace c9c0115ae005805b ]---
```

https://blog.csdn.net/qiangweiloveforever/article/details/8302064

这篇文章描述的跟我的问题类似。



warn_slowpath_common

这个表示的当前运行状态不对，有bug，但是不是致命问题。

```
void warn_slowpath_null(const char *file, int line)
{
 warn_slowpath_common(file, line, __builtin_return_address(0), NULL);
}

#define __WARN() warn_slowpath_null(__FILE__, __LINE__)

#define WARN_ON(condition) ({      \
 int __ret_warn_on = !!(condition);    \
 if (unlikely(__ret_warn_on))     \
  __WARN();      \
 unlikely(__ret_warn_on);     \
})

```

我现在的问题是在nand_wait的最后一行。

```
	status = (int)chip->read_byte(mtd);
	/* This can happen if in case of timeout or buggy dev_ready */
	WARN_ON(!(status & NAND_STATUS_READY));
	return status;
```

我把这个WARN_ON 先注释掉吧。

这样就这个世界都清净了。这个问题就先这样。

# i2c实验

看启动过程的打印：

```
at24 0-0050: 1024 byte 24c08 EEPROM, writable, 16 bytes/write
```

busybox默认集成了i2ctools。

先查看i2c总线的情况。

```
/ # i2cdetect -l
i2c-0   i2c             s3c2410-i2c                             I2C adapter
/ # 
```

可以看到i2c0总线。

然后看看这个总线上的设备情况。

```
/ # i2cdetect -y -r 0
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: UU UU UU UU -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- -- 
```

可以看到地址0x50上，是有设备存在的。就是at24c08这个eeprom。

我们读取里面的内容看看。

```
/ # i2cdump -f -y 0 0x50
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f    0123456789abcdef
00: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
10: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
20: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
30: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
40: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
50: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
60: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
70: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
80: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
90: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
a0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
b0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
c0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
d0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
e0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
f0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
```

现在全部是0xff。

读取其中的一个字节看看。

```
/ # i2cget -f -y 0 0x50 01
0xff
```

写入为0xAA看看。

```
/ # i2cset -f -y 0 0x50 01 0xaa
QEMU ee24c08_tx: write 0001=aa
```

但是再读取出来，还是0xff。

我们看看



看mini2440的bsp文件。

定义了一个bootargs。

```
__setup("mini2440=", mini2440_features_setup);
```

用来选择板子的模式。这种思路值得借鉴。

重点看mini2440_init函数。

```
1、管脚C0配置为LEND复用。是给lcd的背光用的。
2、管脚G4、B1设置。
3、5个按键的初始化。K1到K5，分别在G0、G3、G5、G6、G7上。
4、设置fb。可以跳过。
5、设置usb的udc。
6、设置mmc的。检测脚是G8、写保护脚是H8 。
7、然后是nand的设置。我之前在bootargs里设置的根本就没用。全部是这里设置的。
8、设置i2c0。是在E14和E15上 。
	然后i2c_register_board_info。
9、然后platform_add_devices，把所有的平台设备注册进去，就生成了这些对象。

```

```
/* NAND Flash on MINI2440 board */
static struct mtd_partition mini2440_default_nand_part[] __initdata = {
	[0] = {
		.name	= "u-boot",
		.size	= SZ_256K,
		.offset	= 0,
	},
	[1] = {
		.name	= "u-boot-env",
		.size	= SZ_128K,
		.offset	= SZ_256K,
	},
	[2] = {
		.name	= "kernel",
		/* 5 megabytes, for a kernel with no modules
		 * or a uImage with a ramdisk attached */
		.size	= 0x00500000,
		.offset	= SZ_256K + SZ_128K,
	},
	[3] = {
		.name	= "root",
		.offset	= SZ_256K + SZ_128K + 0x00500000,
		.size	= MTDPART_SIZ_FULL,
	},
};
```

# 三星bsp代码架构

三星的代码写得比较复杂。也是为了较好的兼容性和通用性。

先看看platform_samsumg下的目录结构。

```
teddy@teddy-ubuntu:~/work/linux-rpi/linux-rpi-4.4.y/arch/arm/plat-samsung$ tree -I "*.o"
.
├── adc.c
├── cpu.c
├── devs.c
├── dev-uart.c
├── include
│   └── plat
│       ├── adc-core.h
│       ├── adc.h
│       ├── cpu-freq-core.h
│       ├── cpu-freq.h
│       ├── cpu.h：定义了cpu的ID宏。声明变量samsung_cpu_id。
│       ├── devs.h：声明各种platform_device变量。
│       ├── fb.h
│       ├── fb-s3c2410.h
│       ├── gpio-cfg.h
│       ├── gpio-cfg-helpers.h
│       ├── gpio-core.h
│       ├── iic-core.h
│       ├── keypad.h
│       ├── map-base.h：定义了寄存器在虚拟地址的映射位置，是0xF600 0000。是为了尽量少使用va空间。
│       ├── map-s3c.h
│       ├── map-s5p.h
│       ├── pm-common.h
│       ├── pm.h
│       ├── pwm-core.h
│       ├── regs-adc.h
│       ├── regs-irqtype.h
│       ├── regs-spi.h
│       ├── regs-udc.h
│       ├── samsung-time.h
│       ├── sdhci.h
│       ├── usb-phy.h
│       └── wakeup-mask.h
├── init.c
├── Kconfig
├── Makefile
├── platformdata.c
├── pm.c
├── pm-check.c
├── pm-common.c
├── pm-debug.c
├── pm-gpio.c
├── wakeup-mask.c
└── watchdog-reset.c
```

再看mach-24xx下面的文件。

我只把mini2440用得到的部分列出来。

```
teddy@teddy-ubuntu:~/work/linux-rpi/linux-rpi-4.4.y/arch/arm/mach-s3c24xx$ tree -I "*.o|*.c"
.
├── common.h：这个声明了各种用宏隔开的函数。不怎么优雅。
├── fb-core.h
├── include
│   └── mach
│       ├── dma.h：dam通道名字枚举。
│       ├── fb.h：包含<plat/fb-s3c2410.h>
│       ├── gpio-samsung.h:定义了各种gpio。
│       ├── hardware.h：声明一个函数。
│       ├── io.h：inb、outb等的实现。汇编写的。
│       ├── irqs.h：定义中断号。
│       ├── map.h：物理地址宏。
│       ├── pm-core.h：
│       ├── regs-clock.h
│       ├── regs-gpio.h
│       ├── regs-irq.h
│       ├── regs-lcd.h
│       ├── regs-s3c2443-clock.h
│       ├── rtc-core.h
│       └── s3c2412.h

```

c文件有：

```
├── common.c：定义了很多芯片相关的结构体。
├── cpufreq-utils.c：
├── irq-pm.c
├── mach-mini2440.c
```





# 参考资料

1、Linux ARM IIC I2C EEPROM 读写操作

http://www.voidcn.com/article/p-xirbzczr-bqs.html

