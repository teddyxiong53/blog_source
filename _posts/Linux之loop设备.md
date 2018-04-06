---
title: Linux之loop设备
date: 2018-04-06 14:13:25
tags:
	- Linux

---



#什么是loop设备？

loop设备是一种伪设备。

它可以让我们像块设备一样访问一个文件。

loop这个词怎么理解？

在使用之前，一个loop设备必须要和一个文件进行挂接。

这种结合方式给用户提供了一个替代块特殊文件的接口。

如果这个文件包含一个完整的文件系统，那么这个文件就可以像一个磁盘设备一样被mount。

一般这个是用来mount iso光盘镜像文件的。



# 命令操作示例

1、创建一个软盘。1.44M的大小。

```
dd if=/dev/zero of=./floppy.img bs=512 count=2880 
```

2、使用losetup命令，把这个文件虚拟成块设备。

```
losetup /dev/loop1 floppy.img
```

3、挂载块设备。

```
mount /dev/loop1 /tmp
```

4、卸载。

```
umount /tmp
losetup -d /dev/loop1
```

