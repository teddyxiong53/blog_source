---
title: Linux之recovery分区
date: 2019-05-16 17:16:11
tags:
	- Linux
---



之前做Linux系统，都没有带recovery分区，所以不是很了解。

现在看rk3308是带recovery分区。了解一下。

从编译脚本看， 是把kernel和rootfs打包成这个镜像的。recovery.img文件。

```
$TOP_DIR/kernel/scripts/mkbootimg --kernel $KERNEL_IMAGE --ramdisk $CPIO_IMG --second $KERNEL_DTB -o $TARGET_IMAGE
```

那什么时候可以进入到recovery分区呢？



rootfs要打开recoverySystem支持。

代码在buildroot/external/recovery目录下。

另外还有external/rkupdate。这个主要是解析update.img文件的。



但是这个根文件分区，也不是完整的。而是一个非常简单的。大部分工具都没有。



需要单独的recovery分区，因为这个分区一般是不进行升级的。



入口文件是recovery.c。



怎样进入到recovery分区呢？





参考资料

1、Recovery代码分析之一

https://blog.csdn.net/nbalichaoq/article/details/44035223