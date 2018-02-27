---
title: flash文件系统对比
date: 2017-02-18 22:33:21
tags:
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







到目前为止，工作中使用过的flash文件系统有：yaffs、jffs2、ubifs、squashfs。
yaffs和jffs2是比较常用而且传统的文件系统。yaffs适合在nand flash上使用，而jffs2适合在nor flash上使用。
一般喜欢采用这种混合方式来做，在nor flash里放代码镜像，因为nor flash擦写速度慢，但是读取速度快。
在nand flash里放数据，因为容量大，擦写快。

# 1. cramfs
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

# 2. jffs和jffs2

jffs是瑞典的一家公司开发的，在1999年用GPL协议开源。

是基于linux2.0的。

后面redhat移植到linux2.2上，慢慢发现了很多的问题。于是在2001年，redhat公司决定重新实现jffs，就是jffs2 。

jffs2是一个日志结构的文件系统 。保证了意外调用后数据的完整性。

jffs2是目前flash上使用最多的文件系统。

缺点：

1、挂载时需要扫描整个flash，以确定节点的合法性以及建立必要的数据结构，这就导致了挂载速度慢。

2、将节点信息保存在内存，内存使用和节点数量成正比。

3、用随机的方式来进行磨损平衡。

# 3. yaffs和yaffs2

jffs也可以用在nand上，但是效果不是很好。所以就有了yaffs。

yaffs2是增加了对大容量的nand的支持。

yaffs和jffs的不同：

1、yaffs只借鉴了日志结构的思想，但是没有提供日志功能，所以稳定性不如jffs2，但是资源占用少。

2、yaffs垃圾回收慢一些，但是可以延长nand的寿命。

3、jffs支持压缩，yaffs不支持。

4、yaffs挂载时间更短。





# 4. ubifs
ubifs是2006年发起的一个项目。目标是提高性能、扩展性强的flash专用文件系统。

ubi的字母含义是Unsorted Block Image。是一种类似于lvm的逻辑卷管理层。

主要实现磨损平衡、坏块管理等。

ubifs不直接工作在mtd上，而是工作在ubi卷之上。





# 5. squashfs

squashfs是对cramfs的改进。是一种较新的文件系统，还有待进一步的验证。
生成文件系统时，可以指定`-comp lzo`来用特定的方式来压缩。
默认是用gzip来压缩。squashfs默认就是压缩的。
关于lzo和gzip的压缩效率对比如下：
lzo压缩率比gzip略高，但是压缩和解压速度远高于gzip。所以嵌入式优先选择lzo方式来压缩。

squashfs文件系统最大可以达到`2^64`个字节，支持的单个最大文件可以到2TB。这个是cramfs做不到的。




