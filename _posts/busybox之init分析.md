---
title: busybox之init分析
date: 2018-09-22 16:58:17
tags:
	- Linux

---

--

由于遇到一系列定制，从init开始加载不同服务，对服务异常等需要特殊处理。

如何在恰当的时机加载恰当的服务？

如何对不同异常进行特殊处理？

这就有必要分析内核是如何加载init进程的？

init进程是按照何种顺序启动各种服务的？

init是如何管理这些服务的？

系统开机后各种进程都是在哪里创立的？

带着这些问题来分析一下kernel->init、init进程本身、inittab配置文件、rcS、/etc/profile等等。



在内核启动的最后阶段start_kernel()->reset_init()创建第一个进程，即pid=0的idle进程，

运行在内核态，也是唯一一个没有通过fork()或者kernel_thread()创建的进程。

这个进程最终进入start_kernel()->reset_init()->cpu_startup_entry()->cpu_idle_loop()。



在进程0中生成两个进程：

一个是所有用户空间进程的祖先的init进程，

一个是所有内核线程祖先的kthreadd。



init_main()也即busybox中的init进程入口。

init上承kernel，下起用户空间进程，**配置了整个用户空间工作环境。**



首先初始化串口、环境变量等；

解析/etc/inittab文件；

初始化信号处理函数；

然后依次执行SYSINIT、WAIT、ONCE选项；

**最后在while(1)中监控RESPAWN|ASKFIRST选项。**



/etc/inittab中不同action类型有着先后顺序：SYSINIT > WAIT > ONCE > RESPAWN | ASKFIRST。

run_actions()运行统一action类型的所有命令。但是对于RESPAWN|ASKFIRST特殊处理。



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



参考资料

1、busybox启动流程简单解析：从init到shell login

https://www.cnblogs.com/arnoldlu/p/10868354.html

