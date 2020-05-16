---
title: Linux之mdev
date: 2018-03-07 09:08:00
tags:
	- Linux

---



mdev是mini udev 的缩写。是busybox里的一部分。

文档在busybox/docs/mdev.txt。

mdev有2个基本用途，初始化生成设备和动态更新设备。这2个功能都需要sysfs的支持。要支持动态更新设备，需要使能kernel的热拔插功能。

一般在初始化脚本里写上这个：

```
mount -t proc proc /proc
mount -t sysfs sysfs /sys
echo /sbin/mdev > /proc/sys/kernel/hotplug
mdev -s #开始扫描
```

更完整的写法，会在上面代码的前面再加上这个。

```
mount -t tmpfs -o size=64k,mode=0755 tmpfs /dev #保证/dev是一个tmpfs文件系统。
mkdir /dev/pts
mount -t devpts devpts /dev/pts
```



# 配置文件

在/etc/mdev.conf。

可以没有。有是因为想要修改权限值。

示例：

```
null		0:0 666
zero		0:0 666
urandom		0:0 444

kmem		0:9 000
mem		0:9 640
port		0:9 640

console		0:5 600
ptmx		0:5 660
tty[0-9]*	0:5 660

ttyS[0-9]*	0:20 640

fd[0-9]*	0:11 660

sd[a-z]*	0:6 660
hd[a-z]*	0:6 660

```



# 代码分析

`mdev -s`扫描/sys/class/xxx，查找目录下面有dev这个文件的目录。例如：/sys/class/tty/tty0/dev。这个文件里的内容是：`4:0`。

目录名被当成设备名。