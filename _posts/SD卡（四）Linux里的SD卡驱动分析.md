---
title: SD卡（四）Linux里的SD卡驱动分析
date: 2018-03-06 14:51:53
tags:
	- SD卡

---



# 概念辨析

说到SD卡，总是涉及mmc、sd、sdio这么3个东西。

SD

```
SD是Secure Digital的缩写。是一种卡的标准。用来取代之前的MMC标准。
```

SDIO

```
这个是重点。
SD本来是存储标准，但是可以扩展这个，用来连接一些不是flash的其他设备，例如WiFi芯片。GPS模块。
SDIO是未来嵌入式系统里最重要的接口技术之一。
```

# mmc子系统

mmc子系统在内核的drivers/mmc目录下。

下面有2个子目录。

```
host：针对不同的CPU而不同的。要芯片场景来实现。
core：这个是mmc的核心层。
```

而具体的SD卡，会对应一个client。

这种架构方式，跟i2c的类似。

通信有：

1、命令。host到client。

2、回复。client到host。

3、数据。双向。



命令分类：

```
1、广播，不用回复。
2、广播，需要回复。
3、单播，不带数据。
4、单播，带数据。
```



命令格式：

```
1、6个字节。也就是48个bit。统一看，不分字节看。起始位为0，结束位为1 。
```



sysfs里的情况。

```
/sys/devices/platform/smb@4000000/smb@4000000:motherboard/smb@4000000:motherboard:iofpga@7,00000000/10005000.mmci/mmc_host/mmc0/mmc0:4567 # ls
block                 fwrev                 preferred_erase_size
cid                   hwrev                 scr
csd                   manfid                serial
date                  name                  ssr
driver                ocr                   subsystem
dsr                   oemid                 type
erase_size            power                 uevent
```



# 代码分析

用2.6.35的作为分析对象。

```
include/mmc目录
1、card.h：
	struct mmc_card 
2、core.h
	struct mmc_command
3、host.h
	struct mmc_host_ops
	struct mmc_host
4、mmc.h
	
5、sd.h
	只有几个宏定义。
6、sdio.h
	只有几个宏定义。
7、sdio_func.h
	struct sdio_func
	struct sdio_driver 
8、sdio_ids.h
	只有几个宏定义。
```

所有的函数都以mmc开头的。mmc_xxx_yyy这样。

以三星的为切入口。

入口在这里，注册了一个平台设备。

```
static int __init s3cmci_init(void)
{
	return platform_driver_register(&s3cmci_driver);
}
```

struct s3cmci_host 是核心结构体。

```
{
	struct platform_device *pdev;
	struct mmc_host *mmc;
	
}

```

s3cmci_probe函数。

```
1、mmc_alloc_host
	这个里面INIT_DELAYED_WORK(&host->detect, mmc_rescan);
	这个mmc_rescan是很重要的。
	如果扫描到了，就mmc_attach_mmc。这里面mmc_add_card
	
2、get resource 和irq。
	注册中断s3cmci_irq
3、mmc_add_host 注册mmc host。

```



struct sdhci_s3c 在mmc/host/sdhci-s3c.c里。也很重要。

对应的probe函数里，也申请了一个重点，是检测SD卡状态的中断。

```
ret = request_irq(pdata->ext_cd, sdhci_irq_cd,
				IRQF_SHARED, mmc_hostname(host->mmc), sc);
```



看vexpress-a9的开机时的打印。

```
mmci-pl18x 10005000.mmci: Got CD GPIO
mmci-pl18x 10005000.mmci: Got WP GPIO
mmci-pl18x 10005000.mmci: mmc0: PL181 manf 41 rev0 at 0x10005000 irq 34,35 (pio)
mmc0: new SD card at address 4567
ledtrig-cpu: registered to indicate activity on CPUs
usbcore: registered new interface driver usbhid
usbhid: USB HID core driver
input: AT Raw Set 2 keyboard as /devices/platform/smb@4000000/smb@4000000:motherboard/smb@4000000:motherboard:iofpga@7,00000000/10006000.kmi/serio0/input/input0
mmcblk0: mmc0:4567 QEMU! 64.0 MiB 
```



SD卡需要的gpio有哪些？

1、写保护。

2、状态检测。

刚好这2个脚在外置的时候，都是没有的。标准里也没有写这2个脚。

```
为什么标准SD卡是九根线，而一般原理图上都是11根线或更多呢？
一般10脚是检测卡是否插入，11脚是卡写保护的检测，再有其它引脚就是用于固定卡座的脚了 ，其实简单应用这两个脚都可以不要管的。
```



# 参考资料

1、Linux SD/MMC/SDIO驱动分析

https://www.cnblogs.com/cslunatic/p/3678045.html

2、SD卡封转及管脚说明

http://blog.sina.com.cn/s/blog_6203f2600101bctn.html

