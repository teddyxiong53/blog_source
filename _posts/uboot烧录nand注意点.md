---
title: uboot烧录nand注意点
date: 2017-05-25 19:57:27
tags:

	- nand

---

板子上使用了nand flash，在烧录使用过程中碰到一些问题，记录如下。

# 报ecctype不对

这个需要看uboot启动时打印的信息，看ecctype是什么值，然后在做yaffs文件系统的时候，传递的参数要与这个值一致，不然会无法挂载文件系统。

# kernel里报init错误

这个是因为我用命令写入rootfs.yaffs文件系统镜像到板端时，没有使用nand write.yaffs，而是用普通的nand write写入导致的。

# uboot用nand write.yaffs写入报没有也对齐的错误 

yaffs文件系统镜像，其大小是已经处理过的，。我一直习惯写入一个0x100000字节的整数倍的长度。nand write.yaffs后面跟的长度值，要跟镜像大小是一样的。





# 一款nand分析

一般page是2K，block是128K，64个page构成一个block。

如果一个block里有一个page是坏的，那么整个block就不能用了。

oob一般是128字节。

```
GigaDevice  GD5F1GQ4UB 3.3v SPI NAND was found.
128 MiB, block size: 128 KiB, page size: 2048, OOB size: 128

Creating 7 MTD partitions on "spi-nand0":
0x000000000000-0x000000200000 : "bootloader"
0x000000800000-0x000001000000 : "tpl"
0x000001000000-0x000001040000 : "misc"
0x000001040000-0x000001d40000 : "recovery"
0x000001d40000-0x000002740000 : "boot"
0x000002740000-0x000006f40000 : "system"
0x000006f40000-0x000008000000 : "data"
```

# page size有哪些

一般是2K。

但是可以是：512、2K、4K、8K。



# 参考资料

1、为什么NAND Block中坏一个Page就要丢弃整个Block

http://www.ssdfans.com/?p=2483

2、linux nand 页大小,Linux MTD下获取Nand flash各个参数的过程的详细解析

https://blog.csdn.net/weixin_32016633/article/details/116727772

3、

https://www.micron.com/support/~/media/74C3F8B1250D4935898DB7FE79EB56E7.ashx

4、

https://hikaru092024.pixnet.net/blog/post/82045626-nand-flash-