---
title: flash文件系统对比
date: 2017-02-18 22:33:21
tags:
---
到目前为止，工作中使用过的flash文件系统有：yaffs、jffs2、ubifs、squashfs。
yaffs和jffs2是比较常用而且传统的文件系统。yaffs适合在nand flash上使用，而jffs2适合在nor flash上使用。
一般喜欢采用这种混合方式来做，在nor flash里放代码镜像，因为nor flash擦写速度慢，但是读取速度快。
在nand flash里放数据，因为容量大，擦写快。



