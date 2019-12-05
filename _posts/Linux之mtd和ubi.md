---
title: Linux之mtd和ubi
date: 2019-12-04 14:55:28
tags:
	- Linux
---

1

ubifs是一个新出现的，应用于mtd之上的文件系统。

可以有效地处理坏块和实现磨损平衡。

同时访问速度更快，消耗内存更小。

还有日志功能。

是jffs2的增强版本。

在mtd设备上存在着partition，在ubi上存在volume，他们之间什么关系？

同时也存在着两个概念mtd device，ubi device，他们之间的区别和联系又是什么？



在Linux下的documentation目录下，ubifs.txt里。

ubi是Unsorted Block Images的缩写。

ubifs是一个flash文件系统。专门为flash设备而设计的。

ubifs跟Linux上传统的文件系统都不一样。

ubifs代表了这样一类文件系统，它跟mtd设备一起工作，而不是block设备。

jffs2跟ubifs是一个类型的。



mtd device和block device的区别：

1、mtd device代表flash device，它们由相当大的eraseblock组成（一般是128KB）。

而block device一般是512B。

2、mtd device支持3种操作：

​	在一个eraseblock里，偏移某个值来读取。

​	在一个eraseblock里，偏移某个值来写入。

​	擦除整个eraseblock。

block device支持2种主要操作：

​	读取整个block。

​	写入整个block。

3、eraseblock在写入前需要全部擦除。而block则可以直接写。

4、eraseblock会在多次写入后磨损掉，block则不会。

5、eraseblock可能坏掉（只是对nand），软件必须处理坏块。block则不需要软件处理，硬件会自动处理掉。



ubifs工作在ubi之上。

ubi是一个单独的软件层，代码在drivers/mtd/ubi目录。

ubi提供的volume概念是比mtd device更高层的抽象。



对ubi device的编程模型，跟mtd device的编程模型很像。

ubi device没有磨损和坏块的限制。

在某种意义上，ubifs是下一代的jffs2 。

但是它跟jffs2很不一样，也不兼容。

下面是ubifs和jffs2的区别：

1、jffs2基于mtd device，而ubifs基于ubi。

2、jffs2没有on-media的index，必须在挂载的时候进行构建。这个就需要进行整个flash的扫描。而ubifs则不需要进行扫描。这样就加快了启动速度。

3、jffs2是write-through模式，而ubifs是write-back模式。所以ubifs更快。



跟jffs2类似，ubifs支持实时压缩，这样就占用很小的空间。

跟jffs2一样，ubifs也可以很好地应对意外断电。

不需要fsck.ext2这样的处理。

ubifs自动根据日志进行恢复。保证flash上数据的完整性。



ubifs是对数性能的，因为底层数据结构主要是树。

所以挂载时间和内存消耗，不是随着大小线性递增的。

jffs2也是如此。

这是因为ubifs在flash上维护了文件系统索引。

但是，ubifs是基于ubi的，而ubi是线性的。

所以整体上还是线性的。

但是比jffs2还是要好多了。



ubifs的作者相信，开发完全对数性能的ubi2是可能的。



参考资料

1、

https://blog.csdn.net/oqqyuji12345678/article/details/94616370

2、在Linux下的documentation目录下，ubifs.txt里。