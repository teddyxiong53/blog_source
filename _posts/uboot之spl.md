---
title: uboot之spl
date: 2018-03-02 09:34:58
tags:
	- uboot

---



spl是Secondary Program Loader的缩写。表示第二阶段加载器。

所谓第二阶段，是相当于soc本身的BROM（boot rom）来说的。brom的大小一般32KB左右。

soc启动的时候，最先执行的就是brom里固化的程序。

为什么需要brom？因为soc的SRAM一般也很小，放不下整个的uboot镜像。所以需要brom来初始化ddr内存，把uboot拷贝到ddr里运行。

brom的作用就是把uboot拷贝到内存并运行。

brom就相当于pc系统里的bios的作用。



看最新版本的uboot代码里，spl也支持从nand flash、SD卡等多种设备里启动了。

对应的文档在u-boot/doc/README.SPL。

为了统一所有的当前有的spl实现，uboot增加了spl framework，方便后续的其他芯片添加。

作为spl的所有obj文件，是单独编译的，并且放在一个叫spl的目录下。生成的对应文件是u-boot-spl和u-boot-spo.bin。

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



tq2440板子，没有打开spl这个功能的。

