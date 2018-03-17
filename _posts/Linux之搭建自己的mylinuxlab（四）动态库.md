---
title: Linux之搭建自己的mylinuxlab（四）动态库
date: 2018-03-16 19:33:17
tags:
	- Linux

---



前面为了简化，是把busybox编译成一个静态的文件，所以就不涉及动态库。

那如果要用动态库，应该怎么操作呢？



```
teddy@teddy-ubuntu:/usr/arm-linux-gnueabihf/lib$ cp *.so* ~/work/mylinuxlab/ramfs/lib
```

然后写一个简单的c文件。默认就是连接动态库的。

放到板端运行。不出错。就是对的。

