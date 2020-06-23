---
title: Android系统（四）init进程
date: 2018-01-23 15:03:32
tags:
	- Android系统

---



Android在启动linux内核时传递的bootcmd是这样的：

```
Kernelcommand line: noinitrd root=/dev/nfs console=/dev/ttySAC0 init=/init nfsroot=192.168.1.103:/nfsboot ip=192.168.1.20:192.168.1.103:192.168.1.1:255.255.255.0::eth0:on
```

init进程对应的文件是`system/core/init/init.c`。

init是一切用户进程的父进程。

对应的配置文件是：`system/core/rootdir/init.rc`。

跟linux不同，Android有一个Zygote进程。zygote的字面含义是受精卵。

Zygote进程是Android的核心进程之一。是Android Framework进程家族的祖先。

Zygote是一个典型的C/S架构。其他的进程作为client向Zygote发起请求，Zygote就不断产生Activity进程。



init.rc脚本的语法

由6个部分组成：

```
commands
	一些基本操作。
	例如：
		mkdir /system
		devwait /dev/block/mmcblk0p1
		mount ext4 /dev/block/mmcblk0p1
actions
	表示一系列的commands。
	一般是放在trigger里面。
	
triggers
	on init
		loglevel 3
	这个就是一个trigger的例子。
services
	一般是一个可执行程序。后面跟options，就是它的参数。
options
	services的参数。
properties
	setprop ro.HIDDEN_APP_MEM 5120 
	
```



参考资料

1、Android——init.rc脚本

https://blog.csdn.net/Stephen_yu/article/details/7822916