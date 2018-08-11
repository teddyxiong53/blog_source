---
title: Linux之构建专用linux系统
date: 2018-08-10 20:51:36
tags:
	- Linux

---



总体步骤：

1、添加一块空闲磁盘。

2、下载编译内核。

3、为空闲磁盘安装grub。

我做实验，就在VMware里添加一个新的 硬盘，空间就给1G。

新的磁盘为/dev/sdb。分为3个区：

sdb1：boot。

sdb2：root。

sdb3：swap分区。

```
mkswap /dev/sdb3
```

```
# mkdir -pv /mnt/{boot, sysroot}
# mount /dev/sdb1 /mnt/boot
# mount /dev/sdb2 /mnt/sysroot
# grub-install --root-directory=/mnt /dev/sdb

```



# 参考资料

1、编译内核+BusyBox定制一个Linux提供ssh和web服务

http://blog.51cto.com/chenpipi/1390874