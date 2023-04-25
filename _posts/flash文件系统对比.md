---
title: flash文件系统对比
date: 2017-02-18 22:33:21
tags:
	- 文件系统
---



# flash转换层

vfat、ext等文件系统不能直接在flash上使用，因为无法在flash的同一个位置进行重复的写入操作（必须先进行擦除）。

那么怎样才能在flash上使用ext等文件系统呢？

解决方法就是加一个转换层，叫做FTL。Flash Translation Layer。



一个最简单的FTL实现是把模拟的块设备一一映射到flash上。

当文件系统要写一个flash的扇区时，过程是这样的：

1、把扇区所在块的数据读取到内存。

2、在内存里把数据修改。

3、对块进行擦除。

4、把内存里的数据再写入到flash。



这种方式存在的问题有：

1、效率低。

2、没有提供磨损平衡。容易产生坏块。

3、非常不安全，如果在擦除后掉电了，就导致了这个块的数据丢失。



到目前为止，FTL都不是很好，所以flash要有专门的文件系统。而不是使用ext这种硬盘文件系统。



到目前为止，工作中使用过的flash文件系统有：

yaffs、jffs2、ubifs、squashfs。

yaffs和jffs2是比较常用而且传统的文件系统。

yaffs适合在nand flash上使用，

而jffs2适合在nor flash上使用。

一般喜欢采用这种混合方式来做，

在nor flash里放代码镜像，因为nor flash擦写速度慢，但是读取速度快。

在nand flash里放数据，因为容量大，擦写快。



# cramfs
cramfs是Linus写的一个简单的文件系统，压缩率较好，可以直接从Flash上运行，不用load到内存里。
这个文件系统的只读的。

一些实用操作是

```
#制作镜像
mkcramfs mycramfs/ cramfs.img
#拷贝镜像到flash上。
cp cramfs.img /dev/mtd1
#挂载flash分区
mount -cramfs /dev/mtdblock1 /mnt/nor
```

# jffs和jffs2

jffs是瑞典的一家公司开发的，在1999年用GPL协议开源。

是基于linux2.0的。

后面redhat移植到linux2.2上，慢慢发现了很多的问题。于是在2001年，redhat公司决定重新实现jffs，就是jffs2 。

jffs2是一个日志结构的文件系统 。保证了意外调用后数据的完整性。

jffs2是目前flash上使用最多的文件系统。

缺点：

1、挂载时需要扫描整个flash，以确定节点的合法性以及建立必要的数据结构，这就导致了挂载速度慢。

也因此不适合在大的nand flash上使用。

2、将节点信息保存在内存，内存使用和节点数量成正比。

3、用随机的方式来进行磨损平衡。

4、当文件系统满，或者接近满的时候，会因为垃圾收集，而导致运行速度大大减慢。



## 代码阅读



参考资料

1、

https://blog.csdn.net/kaka__55/article/details/104125663

# yaffs和yaffs2

jffs也可以用在nand上，但是效果不是很好。所以就有了yaffs。

yaffs2是增加了对大容量的nand的支持。

yaffs和jffs的不同：

1、yaffs只借鉴了日志结构的思想，但是没有提供日志功能，所以稳定性不如jffs2，但是资源占用少。

2、yaffs垃圾回收慢一些，但是可以延长nand的寿命。

3、jffs支持压缩，yaffs不支持。

4、yaffs挂载时间更短。





# ubifs
ubifs是2006年发起的一个项目。目标是提高性能、扩展性强的flash专用文件系统。

ubi的字母含义是Unsorted Block Image。是一种类似于lvm的逻辑卷管理层。

主要实现磨损平衡、坏块管理等。

ubifs不直接工作在mtd上，而是工作在ubi卷之上。所以ubifs不能用在SD卡上 。

特性：

1、可预测性。ubifs的挂载时间、内存消耗、io访问时间，都跟flash大小没有关系。所以flash越大，ubifs就越有优势。

2.快速挂载。不会像jffs2那样进行扫描。不受flash大小影响。都是几个ms就完成了挂载。不过ubi的初始化还是跟flash大小有关系。

3、容易异常重启。这样重启只是重做日志，而不需要扫描介质，所以影响也不大。

4、快速压缩。跟jffs2类似，ubifs支持数据压缩存储。

ubifs一般用在nand flash上。



ubifs涉及了3个子系统：

1、mtd子系统。

2、ubi子系统。

3、ubifs。



nand flash，2G的flash为例。

单位分为：

1、page。2048字节+64字节的ecc。

2、block。64个page组成一个block。

3、device。一个flash设备，包含了2048个block。（2G字节）。

我们把flash假想成一个长方体。一个page，就是一个横向的切片。64个切片堆叠起来，就是一个block。

2048个block堆叠起来，得到最后的完整的长方体。



做ubifs，就比较复杂一点。需要涉及的工具有：

1、mkfs.ubifs。

2、ubinize。



之所以要多个工具，因为在uboot里，烧录mkfs.ubifs得到的镜像比较麻烦。

需要：

```
1、uboot需要支持nand flash分区。
2、在uboot里激活这个分区。
3、用ubi write命令来写入。
```

我们借助ubinize工具，就可以得到可以用nand write来直接写入。

mkfs.ubifs需要指定的参数有：

```
1、m。例如2K。
2、x。指定压缩格式。
3、e。逻辑课擦除数目。
4、r或者d。就是rootfs所在的目录。
5、o。指定输出文件名字。
6、c。count。擦除块的个数。
```

举例：

```
mkfs.ubifs -x lzo -m 2k -e 64k -c 2048 -r ./rootfs -o rootfs.ubi
```



ubinize需要指定的参数。

```
[ubifs-volume]
mode=ubi
image=rootfs.ubi
vol_id=0
vol_size=filesize
vol_type=dynamic
vol_name=rootfs
vol_flags=autosize
vol_alignment=1
```

参数解释

```
1、m。最小的单位。
2、p。擦除块的大小。
3、s。subpage的大小。
4、O。VID header offset。
```



举例：

```
ubinize -o rootfs.ubifs -m 2048 -p 64k -s xx -O xx
```

```
Creating 9 MTDpartitions on "NAND":

0x000000000000-0x000000100000: "mtdblock0_u-Boot 1MB "

0x000000100000-0x000001000000 : "mtdbolck1_kernel 15MB"

0x000001000000-0x000002400000: "mtdbolck2_ramdisk 20MB"

0x000002400000-0x000003800000: "mtdblock3_cramfs 20MB"

0x000003800000-0x000006000000: "mtdblock4_jffs2 40MB"

0x000006000000-0x000008800000: "mtdblock5_yaffs2 40MB"

0x000008800000-0x00000b000000: "mtdblock6_ubifs 40MB"

0x00000b000000-0x00000d800000: "mtdblock7_apps 40MB"

0x00000d800000-0x000010000000: "mtdblock8_data 40MB"
```



# squashfs

squashfs是对cramfs的改进。

是一种较新的文件系统，还有待进一步的验证。

生成文件系统时，可以指定`-comp lzo`来用特定的方式来压缩。

默认是用gzip来压缩。squashfs默认就是压缩的。

关于lzo和gzip的压缩效率对比如下：

lzo压缩率比gzip略高，但是压缩和解压速度远高于gzip。所以嵌入式优先选择lzo方式来压缩。

squashfs文件系统最大可以达到`2^64`个字节，支持的单个最大文件可以到2TB。这个是cramfs做不到的。



**squashfs一般用在nor flash上。**

**如果要用在nand flash上。需要修改内核代码，来处理坏块的情况。**



squashfs的制作没有什么特别的。就是可用指定压缩方式。其余跟jffs2这些没有什么不同。



参考资料

1、

https://mrdoc.hjhai.cn/project-4/doc-13/

# 参考资料

1、ubifs笔记

http://www.cnblogs.com/pengdonglin137/p/3398724.html

2、Flash文件系统介绍和平台采用squashfs+ubifs原因

https://blog.csdn.net/yiwuxue/article/details/10464277

3、NAND for SQUASHFS design

https://blog.csdn.net/lwzlemon/article/details/4030463

4、Openwrt学习笔记（二）——Flash Layout and file system

https://blog.csdn.net/lee244868149/article/details/57076615

5、内核移植和文件系统制作（4）：UBIFS根文件系统制作总结

https://blog.csdn.net/u013236359/article/details/38758345



