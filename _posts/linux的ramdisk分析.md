---
title: linux的ramdisk分析
date: 2016-12-02 21:42:26
tags:
	- linux
	- ramdisk
---
linux中可以把一部分的内存mount为分区来使用，通常称之为ramdisk。
有3种方式可以达到这种目的。
1. 使用/dev/ram#
`#`的范围是0到15，这个是在编译内核的时候设置的。
这些ramdisk是虚拟的块设备。你可以像操作硬盘一样来操作它们。例如格式化，挂载，进行文件读写等等。
```
pi@raspberrypi:~ $ sudo mkfs.fat /dev/ram0
mkfs.fat 3.0.27 (2014-11-12)
unable to get drive geometry, using default 255/63
pi@raspberrypi:~ $ sudo mount /dev/ram0 /mnt/ram0
pi@raspberrypi:~ $ cd /mnt/ram0
pi@raspberrypi:/mnt/ram0 $ ls
pi@raspberrypi:/mnt/ram0 $ sudo touch xxx
pi@raspberrypi:/mnt/ram0 $ ls
xxx
pi@raspberrypi:/mnt/ram0 $ 
```
2. ramfs
ramfs处于vfs层，和/dev/ram的不同在于，它自己就是一种文件系统，不需要再另外格式化了。
ramfs默认配置最大使用内存大小的一般。
可以这样来使用ramfs。
```
root@raspberrypi:/mnt# mkdir ramfs
root@raspberrypi:/mnt# mount -t ramfs none /mnt/ramfs
root@raspberrypi:/mnt# ls
lrts  ram0  ramfs  target  teddy0  teddy1  ydyp
root@raspberrypi:/mnt# cd /mnt/ramfs
root@raspberrypi:/mnt/ramfs# ls
root@raspberrypi:/mnt/ramfs# 
root@raspberrypi:/mnt/ramfs# mount
/dev/ram0 on /mnt/ram0 type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=ascii,shortname=mixed,errors=remount-ro)
none on /mnt/ramfs type ramfs (rw,relatime)
```
3. tmpfs
用法如下：
```
root@raspberrypi:/mnt# mkdir tmpfs
root@raspberrypi:/mnt# mount -t tmpfs tmpfs /mnt/tmpfs
root@raspberrypi:/mnt# mount
...
tmpfs on /mnt/tmpfs type tmpfs (rw,relatime)
```


