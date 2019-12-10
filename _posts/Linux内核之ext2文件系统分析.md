---
title: Linux内核之ext2文件系统分析
date: 2019-12-09 11:10:38
tags:
	 - Linux

---

1

Linux正统的文件系统(如ext2、3等)将硬盘分区时会划分出目录块、inode Table区块和data block数据区域。一个文件由一个目录项、inode和数据区域块组成。

Inode包含文件的属性(如读写属性、owner等，以及指向数据块的指针)，数据区域块则是文件内容。当查看某个文件时，会先从inode table中查出文件属性及数据存放点，再从数据块中读取数据。



磁盘的最小存储单元是扇区。512字节。

而文件系统的最小存储单元是block。一般是4KB。

扇区是没法改的。

block是可以在格式化的时候指定。

```
 mke2fs -b 4096 /dev/sda6
```

这样就是指定了block大小为4K。

对于block，因为数量很多，所以就划分了不同的group。

磁盘分区后，总体布局是：

```
| boot block|  block group 0 | block group 1 | ... | block group N|
```

每一个block group的内部是这样：

```
super block
	记录文件系统的信息。
	inode和block的使用数量。
	block和inode的大小。
	文件系统的挂载时间、最近一次写入数据的时间，最近一次fsck的时间。
	validbit，如果是已经挂载了，validbit为0，否则为1.
gdt
	
block bitmap
	块对照表。
	记录哪些block是空闲的。这样就可以快速找到位置来存放数据。
inode bitmap
	inode对照表。
inode table
	inode表格。
data blocks
	存放文件的实际数据。
```

每个block都有一个编号，方便inode进行记录。

一个block，只能被一个文件占有，如果文件很小，block里多余的空间就是浪费的。



dentry是通过将inode编号与文件名相关联来保存inode和文件的粘合剂。



ext2_dir_entry



下面我们进行一些检查的测试。

产生一个名为ext-fs.img的文件。大小为1M。block size为4K。

```
dd if=/dev/zero of=ext2-fs.img bs=4K count=256
```

把这个img文件格式化为ext2格式。

```
mkfs.ext2 ./ext2-fs.img 
```

查看信息：

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ dumpe2fs ./ext2-fs.img 
dumpe2fs 1.42.13 (17-May-2015)
Filesystem volume name:   <none>
Last mounted on:          <not available>
Filesystem UUID:          3b70b775-0501-4539-950c-be431710283c
Filesystem magic number:  0xEF53
Filesystem revision #:    1 (dynamic)
Filesystem features:      ext_attr resize_inode dir_index filetype sparse_super large_file
Filesystem flags:         signed_directory_hash 
Default mount options:    user_xattr acl
Filesystem state:         clean
Errors behavior:          Continue
Filesystem OS type:       Linux
Inode count:              128
Block count:              1024
Reserved block count:     51
Free blocks:              986
Free inodes:              117
First block:              1
Block size:               1024
Fragment size:            1024
Reserved GDT blocks:      3
Blocks per group:         8192
Fragments per group:      8192
Inodes per group:         128
Inode blocks per group:   16
Filesystem created:       Tue Dec 10 13:43:00 2019
Last mount time:          n/a
Last write time:          Tue Dec 10 13:43:00 2019
Mount count:              0
Maximum mount count:      -1
Last checked:             Tue Dec 10 13:43:00 2019
Check interval:           0 (<none>)
Reserved blocks uid:      0 (user root)
Reserved blocks gid:      0 (group root)
First inode:              11
Inode size:               128
Default directory hash:   half_md4
Directory Hash Seed:      e8ad6ebd-9c47-4f62-b640-79e22294ea92


Group 0: (Blocks 1-1023)
  主 superblock at 1, Group descriptors at 2-2
  保留的GDT块位于 3-5
  Block bitmap at 6 (+5), Inode bitmap at 7 (+6)
  Inode表位于 8-23 (+7)
  986 free blocks, 117 free inodes, 2 directories
  可用块数: 38-1023
  可用inode数: 12-128
```

里面只有一个block group。

一个block size，默认是1K字节的。（mkfs.ext2没有指定参数）。

一个group有8192个block。现在不足这个数，所以只有一个block group。

inode的数量是128个。

1024个block编号为1到1024号。

1号block：放superblock。

2号block：放group descriptor。

3到5号：保留的GDT。

6号block：block bitmap。

7号block：inode bitmap。

8到23号block：inode表。



默认每8KB对应一个inode。

挂载看看：

```
sudo mount -o loop ./ext2-fs.img /mymnt
```



```
hlxiong@hlxiong-VirtualBox:/mymnt$ ls -lh
总用量 12K
drwx------ 2 root root 12K 12月 10 13:43 lost+found
```

`lost+found`目录由`e2fsck`工具使用，如果在检查磁盘时发现错误，就把有错误的块挂在这个目录下，因为这些块不知道是谁的，找不到主，就放在这里“失物招领”了。

用winhex打开ext-fs.img文件。

前面1024字节，全部都是0 。这个是启动块。

从0x400到0x7ff，是superblock。



用debugfs打开ext-fs.img文件。

```
debugfs ./ext2-fs.img 
```

这个也是一个交互式工具。输入：

```
stat /
```

结果：

```
debugfs:  stat /
Inode: 2   Type: directory    Mode:  0755   Flags: 0x0
Generation: 0    Version: 0x00000000
User:     0   Group:     0   Size: 1024
File ACL: 0    Directory ACL: 0
Links: 3   Blockcount: 2
Fragment:  Address: 0    Number: 0    Size: 0
ctime: 0x5def3064 -- Tue Dec 10 13:43:00 2019
atime: 0x5def32fc -- Tue Dec 10 13:54:04 2019
mtime: 0x5def3064 -- Tue Dec 10 13:43:00 2019
BLOCKS:
(0):24
TOTAL: 1
```

我现在挂载到mymnt下，然后写一个脚本，创建100个txt文件。

再dumpe2fs看看。

```
Free blocks:              882
Free inodes:              15
Mount count:              2
Maximum mount count:      -1
Lifetime writes:          142 kB

882 free blocks, 15 free inodes, 2 directories
  可用块数: 42-549, 650-1023
  可用inode数: 12, 115-128
```

可以看到还剩15个inode了。

很快就会因为inode耗尽而无法创建文件了。

```
hlxiong@hlxiong-VirtualBox:/mymnt$ sudo touch a b c d e f g h i j k l m n
hlxiong@hlxiong-VirtualBox:/mymnt$ sudo touch o
hlxiong@hlxiong-VirtualBox:/mymnt$ sudo touch p
touch: 无法创建'p': 设备上没有空间
```

```
  可用块数: 42-549, 650-1023
  可用inode数: 
```

**因此在设计时应该尽量避免产生大量琐碎的小文件，大量很小的文件应该把内容放入数据库进行管理。并及时清理临时文件。**



参考资料

1、ext2文件系统中，文件名称和目录名称存在什么地方？

https://q.cnblogs.com/q/43260/

2、Ext2文件系统简单剖析（一）

https://www.jianshu.com/p/3355a35e7e0a

3、Inode与block详解

https://blog.51cto.com/9406836/2124935

4、ext2文件系统结构分析

这篇文章很好。

https://blog.csdn.net/yuzhihui_no1/article/details/50256713