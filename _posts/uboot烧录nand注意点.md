---
title: uboot烧录nand注意点
date: 2017-05-25 19:57:27
tags:

	- nand

---

板子上使用了nand flash，在烧录使用过程中碰到一些问题，记录如下。

# 1. 报ecctype不对

这个需要看uboot启动时打印的信息，看ecctype是什么值，然后在做yaffs文件系统的时候，传递的参数要与这个值一致，不然会无法挂载文件系统。

# 2. kernel里报init错误

这个是因为我用命令写入rootfs.yaffs文件系统镜像到板端时，没有使用nand write.yaffs，而是用普通的nand write写入导致的。

# 3. uboot用nand write.yaffs写入报没有也对齐的错误 

yaffs文件系统镜像，其大小是已经处理过的，。我一直习惯写入一个0x100000字节的整数倍的长度。nand write.yaffs后面跟的长度值，要跟镜像大小是一样的。





