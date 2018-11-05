---
title: Ubuntu之扩展硬盘大小
date: 2018-11-04 00:24:30
tags:
	- Ubuntu

---



我的Ubuntu是在虚拟机里，之前给的空间太小了，只有100G，现在用到80多G。

所以我把硬盘扩展到500G。但是目前看起来，扩展的空间并没有被用起来。

```
teddy@teddy-ubuntu:~$ sudo fdisk /dev/sda
Command (m for help): p
Disk /dev/sda: 500 GiB, 536870912000 bytes, 1048576000 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x5612fa1d

Device     Boot     Start       End   Sectors Size Id Type
/dev/sda1  *         2048 192940031 192937984  92G 83 Linux
/dev/sda2       192942078 209713151  16771074   8G  5 Extended
/dev/sda5       192942080 209713151  16771072   8G 82 Linux swap / Solaris
```

试了一下，从打印提示看，不能把空间弄出来。

算了，我还是选择新增一块硬盘的方式。不要把之前的数据弄坏了。

sdb，大小500G。挂载到/home/teddy/work2目录下。

然后修改/etc/fstab内容。开机时自动挂载。

```
teddy@teddy-ubuntu:~$ df -h
df: /mnt/hgfs: Protocol error
Filesystem      Size  Used Avail Use% Mounted on
udev            2.0G     0  2.0G   0% /dev
tmpfs           394M   15M  379M   4% /run
/dev/sda1        91G   73G   14G  85% /
tmpfs           2.0G     0  2.0G   0% /dev/shm
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/sdb1       493G   70M  467G   1% /home/teddy/work2
tmpfs           394M     0  394M   0% /run/user/1000
```



