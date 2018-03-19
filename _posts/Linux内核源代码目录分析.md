---
title: Linux内核源代码目录分析
date: 2018-03-19 16:18:16
tags:
	- Linux

---



Linux内核源代码虽然文件多，但是实际核心的部分，并不多。

现在分析与具体驱动、bsp无关的代码的目录分布情况。

# block

这个模块我暂时不关注。

下面是80个文件。

# fs



# init

就这13个文件。都很重要。要细读。

```
.
├── calibrate.c 计算lpj。
├── do_mounts.c 挂载rootfs。
├── do_mounts.h 
├── do_mounts_initrd.c
├── do_mounts_md.c 
├── do_mounts_rd.c 
├── initramfs.c
├── init_task.c 
├── Kconfig
├── main.c ：入口。start_kernel在这里。
├── Makefile
├── noinitramfs.c
└── version.c
```

# ipc

14个文件。重要。

```
├── compat.c
├── compat_mq.c
├── ipc_sysctl.c
├── Makefile
├── mq_sysctl.c
├── mqueue.c
├── msg.c
├── msgutil.c
├── namespace.c
├── sem.c
├── shm.c
├── syscall.c
├── util.c
└── util.h
```



# kernel

300个文件左右。重要。



# mm

100个文件。

重要。



