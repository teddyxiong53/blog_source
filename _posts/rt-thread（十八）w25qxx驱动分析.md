---
title: rt-thread（十八）w25qxx驱动分析
date: 2018-02-13 13:35:37
tags:
	- rt-thread

---



 w25qxx是一个常见的spi flash芯片。我以这个为切入口，来分析rt-thread里的flash驱动相关内容。

内容在components/drivers/spi目录下。

下面有两份w25qxx的内容。一个是spi_flash_w25qxx.c，一个是spi_flash_w25qxx_mtd.c。这2个的关系是什么？是依赖还是并列？

```
if GetDepend('RT_USING_W25QXX'):
    src_device += ['spi_flash_w25qxx.c']
    
if GetDepend('RT_USING_W25QXX_MTD'):
    src_device += ['spi_flash_w25qxx_mtd.c']  
```

目前看不出来。我们先继续看。

从spi_flash_w25qxx.c这个开始看。

# w25qxx_init

输入：2个参数。

一个是flash的名字。我们可以叫spiflash0 。

一个是spi的名字。我们可以叫spi0 。

假设spiflash0就挂在spi0这个总线上。

所以设备工作的前提是spi0总线已经注册进去了。这个代码是在bsp目录下做。因为跟芯片是紧密相关的。

w25qxx的spi模式是，模式0，msb。



把所有代码大概过了一下，发现spi_flash_w25qxx.c和spi_flash_w25qxx_mtd.c是并列的关系。

mtd的也没有发现特别的地方。

因为mtd的目前是空实现。

