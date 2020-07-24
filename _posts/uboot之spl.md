---
title: uboot之spl
date: 2018-03-02 09:34:58
tags:
	- uboot

---



spl是Secondary Program Loader的缩写。表示第二阶段加载器。

**所谓第二阶段，是相当于soc本身的BROM（boot rom）来说的。**brom的大小一般32KB左右。

soc启动的时候，最先执行的就是brom里固化的程序。

为什么需要brom？因为soc的SRAM一般也很小，放不下整个的uboot镜像。所以需要brom来初始化ddr内存，把uboot拷贝到ddr里运行。

brom的作用就是把uboot拷贝到内存并运行。

brom就相当于pc系统里的bios的作用。



**看最新版本的uboot代码里，spl也支持从nand flash、SD卡等多种设备里启动了。**

对应的文档在u-boot/doc/README.SPL。

为了统一所有的当前有的spl实现，uboot增加了spl framework，方便后续的其他芯片添加。

**作为spl的所有obj文件，是单独编译的，并且放在一个叫spl的目录下**。生成的对应文件是u-boot-spl和u-boot-spo.bin。

对应的开关是CONFIG_SPL_BUILD。

```
ifeq ($(CONFIG_SPL_BUILD),y)
obj-y += board_spl.o
else
obj-y += board.o
endif
```

还有一个CONFIG_SPL的选项。

还需要但都的连接脚本CONFIG_SPL_LDSCRIPT。不同的textbase。CONFIG_SPL_TEXT_BASE。

还有一些模块可以加入到spl里。对应的配置项是：

```
CONFIG_SPL_I2C_SUPPORT
...
```





# TPL

TPL是Third Program Loader。第三阶段加载器。

对应的文档在u-boot/doc/README.TPL。

出现的原因是，有些板子上的spl有大小限制，而且不能兼容所有的外部设备。





对于S3C2410、S3C2440处理器，它们内部有4K的SRAM，当使用Nor Flash启动时，地址为0x40000000；当使用Nand Flash启动时，地址为0。

对于S3C2410、S3C2440开发板，一般都外接64M的SDRAM。SDRAM能被使用之前，需要经过初始化。

所以，先把一个init.bin下载到内部SRAM去运行，它执行SDRAM的初始化；然后再下载一个比较大的程序，比如u-boot到SDRAM去动行，它将实现对Nor、Nand Flash的操作。



**tq2440板子，没有打开spl这个功能的。**





SPL（Secondary programloader）是uboot第一阶段执行的代码。

主要负责搬移uboot第二阶段的代码到系统内存（System Ram，也叫片外内存）中运行。

SPL是由固化在芯片内部的ROM引导的。

我们知道很多芯片厂商固化的ROM支持从nandflash、SDCARD等外部介质启动。

**所谓启动，就是从这些外部介质中搬移一段固定大小（4K/8K/16K等）的代码到内部RAM中运行。**

这里搬移的就是SPL。

在最新版本的uboot中，可以看到SPL也支持nandflash，SDCARD等多种启动方式。

当SPL本身被搬移到内部RAM中运行时，它会从nandflash、SDCARD等外部介质中搬移uboot第二阶段的代码到系统内存中。

SPL复用的是uboot里面的代码.



上文中说道“SPL复用的是uboot里面的代码”，那要生成我们所需要的SPL目标文件，我们又该如何下手呢？

很容易想到，通过编译选项便可以将SPL和uboot代码分离、复用。

这里所说的编译选项便是CONFIG_SPL_BUILD，在make Kconfig的时候使能。

最终编译生成的SPL二进制文件有u-boot-spl，u-boot-spl.bin以及u-boot-spl.map。



参考资料

1、

https://blog.csdn.net/rikeyone/article/details/51646200	

2、ARM U-Boot SPL过程浅析

https://blog.csdn.net/jxgz_leo/article/details/52098776