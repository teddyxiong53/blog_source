---
title: Linux之cloud-lab（五）模块实验
date: 2018-03-08 14:04:00
tags:
	- Linux
	- cloud-lab

---



1、准备。

```
#编译
make modules m=ldt
#安装
make modules-install m=ldt
#重新打包文件系统
make root-rebuild
#运行系统
make boot
```

本来编译kthread_sample.c会报错。我先把这个模块不编译。

2、加载驱动。

```
cd /lib/modules/4.14.0+/extra
insmod ./ldt.ko
```

现在报错了。

```
说是尝试去free一个已经是free的irq，是uart的irq，中断号是4 。
```

看看代码。

