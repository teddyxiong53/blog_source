---
title: flash文件系统对比
date: 2017-02-18 22:33:21
tags:
---
到目前为止，工作中使用过的flash文件系统有：yaffs、jffs2、ubifs、squashfs。
yaffs和jffs2是比较常用而且传统的文件系统。yaffs适合在nand flash上使用，而jffs2适合在nor flash上使用。
一般喜欢采用这种混合方式来做，在nor flash里放代码镜像，因为nor flash擦写速度慢，但是读取速度快。
在nand flash里放数据，因为容量大，擦写快。

# 1. cramfs
cramfs是Linus写的一个简单的文件系统，压缩率较好，可以直接从Flash上运行，不用load到内存里。
这个文件系统的只读的。

# 2. squashfs
squashfs是对cramfs的改进。是一种较新的文件系统，还有待进一步的验证。
生成文件系统时，可以指定`-comp lzo`来用特定的方式来压缩。
默认是用gzip来压缩。squashfs默认就是压缩的。
关于lzo和gzip的压缩效率对比如下：
lzo压缩率比gzip略高，但是压缩和解压速度远高于gzip。所以嵌入式优先选择lzo方式来压缩。

squashfs文件系统最大可以达到`2^64`个字节，支持的单个最大文件可以到2TB。这个是cramfs做不到的。



# 3. ubifs
这个文件系统的生成时，需要指定的参数较多。




