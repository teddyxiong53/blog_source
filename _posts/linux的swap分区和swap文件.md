---
title: linux的分区
date: 2016-12-12 20:00:26
tags:
	- linux
	- 分区
---
linux上IDE硬盘最多接4个，名字分别是hda、hdb、hdc、hdd。每个硬盘上的分区数最多是63个。例如hda1一直到hda63 。而其中主分区个数不能超过4个。扩展分区最多只能有一个。扩展分区里的逻辑分区个数可以是多个。
SCSI接口的硬盘个数是16个，名字sd[a-p]。每个硬盘上的分区数最多是15个，例如从sda1到sda15 。
这个信息可以从linux源代码的Documentation/devices.txt里找到。


这个是我的Ubuntu的配置，硬盘总大小是100G。
用`fdisk -l`查看。一个主分区96.3G，一个扩展分区，扩展分区里是一个逻辑分区（这个分区是swap分区）。
```
设备       启动     Start    末尾    扇区  Size Id 类型
/dev/sda1  *         2048 201877503 201875456 96.3G 83 Linux
/dev/sda2       201879550 209713151   7833602  3.8G  5 扩展
/dev/sda5       201879552 209713151   7833600  3.8G 82 Linux 交换 / Solaris
```
不能直接格式化扩展分区，只能格式化主分区和逻辑分区。
所以对于一个扩展分区，要么删掉新建一个主分区，要么就在该扩展分区上新建一个逻辑分区。
逻辑分区的计数从5开始。

看/etc/fstab里，并没有指定一个/dev/sda1这样的设备名。而是一个uuid。
在之前的linux版本里，的确就是把/dev/sda1这样的设备名写在fstab里，但是这样做有隐患，可能重启后分区的设备名会变动，导致系统出现异常。
在linux系统里，每个块设备都有一个全局唯一的uuid，用这个uuid来替换设备名，就可以避免混乱了。

```
teddy@teddy-ubuntu:/etc$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
fd0      2:0    1    4K  0 disk 
sda      8:0    0  100G  0 disk 
├─sda1   8:1    0 96.3G  0 part /
├─sda2   8:2    0    1K  0 part 
└─sda5   8:5    0  3.8G  0 part [SWAP]
sr0     11:0    1 1024M  0 rom  
teddy@teddy-ubuntu:/etc$ blkid    
/dev/sda5: UUID="5cf11d05-4df0-4ccd-8657-09b3bfbd30ab" TYPE="swap" PARTUUID="9adf8103-05"
```

