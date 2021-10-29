---
title: Linux之tmpfs的shm
date: 2018-03-07 13:36:33
tags:
	- Linux

---



# 跟ramdisk比较

/dev/shm跟ramdisk不同。shm是一个tmpfs。

而ramdisk是一个块设备，对于的设备是/dev/ram0这样的。你需要把mkfs /dev/ram0才能用。



# tmpfs的优点

1、动态文件系统的大小。

2、速度快。



# 修改shm大小

默认是内存大小的一半，而且默认的inode数量不多，我们可以用mount来重新挂载。

```
mount -o size=1500M -o nr_inodes=1000000 -o noatime,nodiratime -o remount /dev/shm
```

这个改动只是临时的，如果想要永久改动。

在/etc/fstab里加上。

```
tmpfs /dev/shm tmpfs defaults,size=1.5G 0 0 
```

# 应用

我看树莓派上默认/tmp目录，是磁盘上的，并不是tmpfs的。

可以用/dev/shm来做。

```
mkdir /dev/shm/tmp
chmod 1777 /dev/shm/tmp
mount -bind /dev/shm/tmp /tmp
```

查看shm的大小。

```
pi@raspberrypi:/tmp$ df -h /dev/shm
Filesystem      Size  Used Avail Use% Mounted on
tmpfs           463M     0  463M   0% /dev/shm
```



