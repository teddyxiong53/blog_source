---
title: Linux之虚拟磁盘
date: 2018-08-10 21:03:43
tags:
	- Linux

---



要做一个简单实验，要磁盘设备，看看如何虚拟一个出来。

```
dd if=/dev/zero of=./fake_disk.img bs=1M count=32
```

```
sudo losetup /dev/loop0 ./fake_disk.img 
```



# 参考资料

1、Linux虚拟磁盘映像创建过程

https://blog.csdn.net/u014674798/article/details/52637082