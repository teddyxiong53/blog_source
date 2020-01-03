---
title: uboot之设备树
date: 2018-03-03 22:17:07
tags:
	- uboot

---

1

Uboot mainline 从 v1.1.3开始支持Device Tree，其对ARM的支持则是和ARM内核支持Device Tree同期完成。

为了使能Device Tree，需要编译Uboot的时候在config文件中加入#define CONFIG_OF_LIBFDT

在Uboot中，可以从NAND、SD或者TFTP等任意介质将.dtb读入内存，假设.dtb放入的内存地址为0x71000000，之后可在Uboot运行命令fdt addr命令设置.dtb的地址，如：
U-Boot> fdt addr 0x71000000

fdt的其他命令就变地可以使用，如fdt resize、fdt print等。



对于ARM来讲，可以透过bootz kernel_addr initrd_address dtb_address的命令来启动内核，**即dtb_address作**

**为bootz或者bootm的最后一次参数，**第一个参数为内核映像的地址，第二个参数为initrd的地址，若不存在

initrd，可以用 -代替。       



http://blog.csdn.net/abcamus/article/details/53890694

