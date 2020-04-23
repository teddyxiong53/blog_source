---
title: linux的ramdisk分析
date: 2016-12-02 21:42:26
tags:
	- linux
	- ramdisk
---


# ramdisk的优点

ramdisk在嵌入式系统上很常用。有这些优点：

1、大家都知道。

2、linux 内核很支持。

3、构造简单。

4、容易使用。你可以把ramdisk跟kernel镜像打包在一起。

5、基于ram ，速度快。

6、可写。

7、掉电不保存，也就没法被破坏。

# ramdisk的缺点

1、占用较多的内存。

2、导致开机速度变慢。

3、需要额外空间来保存。



# 操作

当使用initrd的时候，按照这个顺序启动。

1、uboot载入kernel和ramdisk。

2、kernel把initrd转成一个正常的ram disk，释放initrd占用的内存。

3、如果rootdev不是/dev/ram0，会调用change_root。

4、rootdev挂载了。如果是/dev/ram0，initrd被挂载为root。

5、执行init。在init里挂载真正的root文件系统。



# boot选项

1、initrd=path。

2、noinitrd

3、root=/dev/ram0 rw



# 使用场景







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



# 参考文章

1、uboot官网

https://www.denx.de/wiki/DULG/RootFileSystemOnARamdisk

2、

https://www.kernel.org/doc/html/v4.12/admin-guide/initrd.html

3、

https://www.ibm.com/developerworks/library/l-initrd/

