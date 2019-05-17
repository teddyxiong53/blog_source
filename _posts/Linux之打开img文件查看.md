---
title: Linux之打开img文件查看
date: 2019-05-17 09:04:11
tags:
	- Linux
---



现在有一个recovery.img文件，想打开看看里面有什么内容。

```
hlxiong@hlxiong-VirtualBox:~/work2/rk3308_repo/rockdev$ fdisk recovery.img

Welcome to fdisk (util-linux 2.27.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0x8e8c8ad6.

命令(输入 m 获取帮助)： p
Disk recovery.img: 10.1 MiB, 10575872 bytes, 20656 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x8e8c8ad6
```

挂载rootfs.img的可以。

```
hlxiong@hlxiong-VirtualBox:~/work2/rk3308_repo/rockdev$ sudo mount -o loop ./rootfs.img /mnt
hlxiong@hlxiong-VirtualBox:~/work2/rk3308_repo/rockdev$ cd /mnt
hlxiong@hlxiong-VirtualBox:/mnt$ ls
bin  data  dev  etc  lib  lib64  linuxrc  media  mnt  oem  opt  proc  root  run  sbin  sdcard  sys  system  tmp  udisk  userdata  usr  var
```

但是recovery.img的不行。



参考资料

1、linux系统中如何打开察看img文件内容

https://blog.csdn.net/flfihpv259/article/details/53941096

