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

