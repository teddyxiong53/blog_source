---
title: avs之树莓派环境搭建
date: 2018-10-14 10:39:51
tags:
	- avs
	- 树莓派

---



需要的东西：

1、usb的麦克风。我有一个usb摄像头，上面带麦克风。

2、3.5mm的音箱。用耳机也可以的。



当前我在Ubuntu笔记本上已经完整把avs跑起来了。带屏版本也跑起来了。

但是还有led控制，蓝牙功能这些，通过笔记本不方便进行测试。

所以还是要在树莓派上跑起来。

完全重新安装镜像到一个U盘上，这样从头开始。

最新的是2018年10月9日更新的。代号是stretch。

烧录后，树莓派系统居然不运行。换个usb口就好了。

但是还是有不对的地方，为什么U盘没有都被用起来。我U盘是16G的。

```
pi@raspberrypi:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       1.7G  1.1G  521M  67% /
devtmpfs         54M     0   54M   0% /dev
tmpfs            58M     0   58M   0% /dev/shm
tmpfs            58M  1.8M   56M   4% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs            58M     0   58M   0% /sys/fs/cgroup
/dev/sda1        44M   22M   22M  51% /boot
tmpfs            12M     0   12M   0% /run/user/1000
```

```
sudo raspi-config
```

不行，这个只能调整SD卡的大小。不能调整U盘的。

Linux下调试根分区大小非常麻烦。

我在Linux环境下，把U盘的分区都删掉。我怀疑可能是我之前在windows下格式化U盘导致的。

不是，我再次试了一下，还是这样。

```
pi@raspberrypi:~$ sudo fdisk -l /dev/sdb

Disk /dev/sdb: 14.9 GiB, 15938355200 bytes, 31129600 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xee25660b

Device     Boot Start     End Sectors  Size Id Type
/dev/sdb1        8192   97889   89698 43.8M  c W95 FAT32 (LBA)
/dev/sdb2       98304 3645439 3547136  1.7G 83 Linux
```

是这个工具的问题吗？

用这个工具试一下。

https://www.balena.io/etcher/



用这个工具还是这样。

https://www.cnblogs.com/mfryf/p/5047787.html

```
sudo apt-get install lvm2
```

感觉是U盘有了问题。怎么都扩展不了。

算了，还是在之前的基础上，把新的U盘挂载上去。



# 参考资料

1、官方教程

