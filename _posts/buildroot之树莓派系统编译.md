---
title: buildroot之树莓派系统编译
date: 2019-05-17 13:27:11
tags:
	- Linux
---



配置：

```
make raspberrypi3_defconfig
```

编译：

```
make ARCH=arm -j16
```

在output目录下，得到sdcard.img文件。

把这个文件用工具烧录到SD卡里。

就可以用这个卡来启动了。



看看配置文件。

是会下载专门的内核。

```
BR2_LINUX_KERNEL_CUSTOM_REPO_URL="https://github.com/raspberrypi/linux.git"
BR2_LINUX_KERNEL_CUSTOM_REPO_VERSION="33ee56d5927ceff630fbc87e3f5caa409b6ae114"
BR2_LINUX_KERNEL_DEFCONFIG="bcm2709"
```

指定dtb。

```
BR2_LINUX_KERNEL_DTS_SUPPORT=y
BR2_LINUX_KERNEL_INTREE_DTS_NAME="bcm2710-rpi-3-b bcm2710-rpi-cm3"
```

一些特殊的脚本。

```
BR2_ROOTFS_POST_BUILD_SCRIPT="board/raspberrypi3/post-build.sh"
BR2_ROOTFS_POST_IMAGE_SCRIPT="board/raspberrypi3/post-image.sh"
BR2_ROOTFS_POST_SCRIPT_ARGS="--add-pi3-miniuart-bt-overlay"
```

我make menuconfig看一下，发现默认用的是uclibc，我改成glibc的。

默认也没有使用uboot。

board目录下的配置，都是同一个目录。

```
raspberrypi
raspberrypi0 -> raspberrypi
raspberrypi2 -> raspberrypi
raspberrypi3 -> raspberrypi
raspberrypi3-64 -> raspberrypi
```





参考资料

1、Buildroot构建树莓派轻量级的Linux根文件系统

https://blog.csdn.net/apiculate/article/details/79257789

