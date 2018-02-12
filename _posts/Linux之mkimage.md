---
title: Linux之mkimage
date: 2018-02-11 10:17:37
tags:
	- Linux

---



mkimage的选项：

```
-A：指定ARCH
-O：指定os
-T：指定image type
-C：指定压缩type
-a：指定load addr
-e：指定entry addr
-n：指定镜像的name
-x：设置是否XIP。
-d：从哪个data文件里来数据。
#查看类的：
-l：查看当前镜像的信息。
```

举例：把zImage做成uImage。其实就是加了一个64字节的头部。头部信息就是arch、os这些信息。

```
mkimage -A arm -O linux -T kernel -C none -a 0x30008000 -e 0x30008000 -n "MyLinux" -d zImage uImage
```





