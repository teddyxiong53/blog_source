---
title: busybox之init分析
date: 2018-09-22 16:58:17
tags:
	- Linux

---



关于linuxrc

```
//config:config LINUXRC
//config:	bool "linuxrc: support running init from initrd (not initramfs)"
//config:	default y
//config:	select FEATURE_SYSLOG
//config:	help
//config:	Legacy support for running init under the old-style initrd. Allows
//config:	the name linuxrc to act as init, and it doesn't assume init is PID 1.
//config:
//config:	This does not apply to initramfs, which runs /init as PID 1 and
//config:	requires no special support.
```

init对于理解Linux文件系统的启动过程很有用。值得花大力气深入学习。



看init.c文件。

```
/* Start these actions first and wait for completion */
#define SYSINIT     0x01
/* Start these after SYSINIT and wait for completion */
#define WAIT        0x02
/* Start these after WAIT and *dont* wait for completion */
#define ONCE        0x04
```



