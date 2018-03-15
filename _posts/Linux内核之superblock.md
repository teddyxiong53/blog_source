---
title: Linux内核之superblock
date: 2018-03-15 14:06:30
tags:
	- Linux内核

---



superblock、inode、dentry、file，都属于元数据（metadata）。

所谓元数据，就是data about data。



superblock是文件系统里最基本的元数据。

对于文件系统是非常关键的。所以每个文件系统都对superblock进行了多个冗余备份。

例如，如果/var分区对应的superblock损坏了，那么/var分区就无法挂载。

这个时候，会自动执行fsck来自动选择一份备份的superblock，并尝试修复文件系统。

在我的树莓派上。查看superblock。

```
pi@raspberrypi:~$ sudo dumpe2fs /dev/sdb1 |grep -i superblock
dumpe2fs 1.42.12 (29-Aug-2014)
  Primary superblock at 0, Group descriptors at 1-1
  Backup superblock at 32768, Group descriptors at 32769-32769
  Backup superblock at 98304, Group descriptors at 98305-98305
  Backup superblock at 163840, Group descriptors at 163841-163841
  Backup superblock at 229376, Group descriptors at 229377-229377
  Backup superblock at 294912, Group descriptors at 294913-294913
  Backup superblock at 819200, Group descriptors at 819201-819201
  Backup superblock at 884736, Group descriptors at 884737-884737
  Backup superblock at 1605632, Group descriptors at 1605633-1605633
pi@raspberrypi:~$ 
```

可以看到分为Primary superblock和Backup superblock。



inode则是一个磁盘文件的元数据。

dentry则是把inode和file关联到一起的粘合剂。



做一个形象的比喻，这个超级块就好像是企业的资产负债表，一个文件系统中有哪些资源都记录在这个表中。

OS启动后，内核把把superblock的内容拷贝到内存里，并且周期性地把内存里的superblock更新到磁盘上的superblock里去。

但是这个有一个时间差。

如果意外断电，轻则文件丢失，重则文件系统损坏。

sync命令可以出发这个同步。

