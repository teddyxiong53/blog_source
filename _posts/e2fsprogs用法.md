---
title: e2fsprogs用法
date: 2023-03-09 13:53:31
tags:
	- 文件系统

---



# 概述

**e2fsprogs**（又称为**e2fs programs**）是用以维护[ext2](https://zh.wikipedia.org/wiki/Ext2)，[ext3](https://zh.wikipedia.org/wiki/Ext3)和[ext4](https://zh.wikipedia.org/wiki/Ext4)[档案系统](https://zh.wikipedia.org/wiki/檔案系統)的工具程序集。

由于ext2/3/4是绝大多数[Linux发行版](https://zh.wikipedia.org/wiki/Linux发行版)默认的文件系统，所以这套工具集也包含在众多Linux发行版内。



e2fsprogs包含以下独立的程式：

- `e2fsck`, ext2/3/4文件系统的[fsck](https://zh.wikipedia.org/wiki/Fsck)程序，用于检查文件系统的完整性。
- `mke2fs`, 用于创建ext2/3/4档案系统。
- `resize2fs`, 调整已建立的ext2/3/4档案系统的大小。
- `tune2fs`, 修改ext2/3/4档案系统的相关参数。
- `dumpe2fs`, 显示ext2/3/4档案系统的相关资讯。
- `debugfs`, 用于调试ext2/3/4文件系统，可以查看与更改文件系统的状态。

e2fsprogs工具集同时也包含函数库[libext2fs](https://zh.wikipedia.org/w/index.php?title=Libext2fs&action=edit&redlink=1)。



```
 e2fsck ./rootfs.ext2
e2fsck 1.45.5 (07-Jan-2020)
./rootfs.ext2: clean, 2632/65536 files, 45081/262144 blocks
```

所以这个意思是说，最多65536个文件？

262144个block。一个block多大？4K。

哪里指定的？

通过-b选项指定，没有指定，默认就是4K。

```
/usr/sbin/mkfs.ext2 -> mke2fs
```



```
mke2fs 
[-cFMqrSvV]
	-c 检测是否有损坏的block。
	-F force指定，不管device的类型。
	-M 记录最后一次mount的目录。
	-q  quiet模式，不打印信息。
	-r 指定ext的版本。
	-S 只写入superblock和group描述符。
	
[-b <区块大小>]
[-f <不连续区段大小>]
[-i <字节>]
[-N <inode数>]
[-l <文件>]
[-L <标签>]
[-m <百分比值>]
[-R=<区块数>]
[ 设备名称]
[区块数]
```



使用mkfs.ext4默认参数格式化磁盘后，

发现格式化时间特别长，

并且格式化会占用磁盘很大的空间。

例如2TB的磁盘格式化会占用10分钟左右时间，

并占用30G左右的磁盘空间。

究其原因，原来inode会占用磁盘空间，

每个inode占用256b大小空间。

默认情况下，mkfs2fs会为每16kb的磁盘空间分配一个inode，

格式化时系统根据磁盘大小，计算可以保存的文件个数，进而为inode保留空间。

所以格式化大容量磁盘，系统会分配过多inode，为inode预留过多空间，导致磁盘空间占用特别大。



通过以上信息可以计算出磁盘格式化后inode占用的磁盘空间
122101760 * 256 / 1024 / 1024 = 29810mb
inode数量 122101760
乘以
每个inode占用的空间 256b
除以
1024 换算为kb
再除以
1024 换算为 mb
通过以上计算可以得出结论：磁盘空间很大的磁盘使用默认参数格式化磁盘会占用大量磁盘空间，浪费磁盘空间。



mkfs.ext4有参数-i，可以指定：多大磁盘空间分配一个inode



-m选项的真实作用，保留一些block应急使用。默认保留了5%的空间。

```
-m reserved-blocks-percentage
              Specify the percentage of the filesystem blocks reserved for the super-user.  This avoids fragmentation, and allows root-owned daemons, such  as  sys‐
              logd(8), to continue to function correctly after non-privileged processes are prevented from writing to the filesystem.  The default percentage is 5%.
```



# tune2fs

```
$ tune2fs -l ./rootfs.ext2
tune2fs 1.45.5 (07-Jan-2020)
Filesystem volume name:   <none>
Last mounted on:          <not available>
Filesystem UUID:          e21b4ad5-a7f5-41b8-9fc4-7d3bf1392b92
Filesystem magic number:  0xEF53
Filesystem revision #:    1 (dynamic)
Filesystem features:      has_journal ext_attr resize_inode dir_index filetype extent flex_bg sparse_super large_file huge_file dir_nlink extra_isize metadata_csum
Filesystem flags:         signed_directory_hash 
Default mount options:    user_xattr acl
Filesystem state:         clean
Errors behavior:          Continue
Filesystem OS type:       Linux
Inode count:              65536
Block count:              262144
Reserved block count:     13107
Free blocks:              217063
Free inodes:              62904
First block:              0
Block size:               4096
Fragment size:            4096
Reserved GDT blocks:      63
Blocks per group:         32768
Fragments per group:      32768
Inodes per group:         8192
Inode blocks per group:   512
Flex block group size:    16
Filesystem created:       Mon Sep  5 10:41:58 2022
Last mount time:          n/a
Last write time:          Thu Mar  9 16:55:34 2023
Mount count:              0
Maximum mount count:      -1
Last checked:             Mon Sep  5 10:41:58 2022
Check interval:           0 (<none>)
Lifetime writes:          131 MB
Reserved blocks uid:      0 (user root)
Reserved blocks gid:      0 (group root)
First inode:              11
Inode size:               256
Required extra isize:     32
Desired extra isize:      32
Journal inode:            8
Default directory hash:   half_md4
Directory Hash Seed:      9f27b423-d166-499b-bff8-f1b922235b2d
Journal backup:           inode blocks
Checksum type:            crc32c
Checksum:                 0xa3a610b8
```



# 参考资料

1、维基百科

https://zh.wikipedia.org/zh-hans/E2fsprogs

2、Linux mke2fs命令

https://www.runoob.com/linux/linux-comm-mke2fs.html

3、

https://www.cnblogs.com/micmouse521/p/8064568.html