---
title: busybox编译过程梳理
date: 2016-12-20 19:40:12
tags:
	- busybox

---



# 目标之间的依赖关系
```
all: busybox doc

busybox: busybox_unstripped

busybox_unstripped: $(busybox-all) FORCE

busybox-all  := $(core-y) $(libs-y)

core-y		:= \
		applets/ \

libs-y		:= \
		archival/ \
		archival/libarchive/ \
		console-tools/ \
		coreutils/ \
		...
		
core-y: applets/built-in.o

libs-y:
	archival/lib.a  archival/libarchive/lib.a  console-tools/lib.a  coreutils/lib.a  coreutils/libcoreutils/lib.a  
	debianutils/lib.a  e2fsprogs/lib.a  editors/lib.a  findutils/lib.a  init/lib.a  libbb/lib.a  libpwdgrp/lib.a  
	loginutils/lib.a  mailutils/lib.a  miscutils/lib.a  modutils/lib.a  networking/lib.a  networking/libiproute/lib.a
	networking/udhcp/lib.a  printutils/lib.a  procps/lib.a  runit/lib.a  selinux/lib.a  shell/lib.a  sysklogd/lib.a 
	util-linux/lib.a  util-linux/volume_id/lib.a  archival/built-in.o  archival/libarchive/built-in.o  console-tools/built-in.o
	coreutils/built-in.o  coreutils/libcoreutils/built-in.o  debianutils/built-in.o  e2fsprogs/built-in.o  editors/built-in.o 
	findutils/built-in.o  init/built-in.o  libbb/built-in.o  libpwdgrp/built-in.o  loginutils/built-in.o  mailutils/built-in.o 
	miscutils/built-in.o  modutils/built-in.o  networking/built-in.o  networking/libiproute/built-in.o  networking/udhcp/built-in.o
	printutils/built-in.o  procps/built-in.o  runit/built-in.o  selinux/built-in.o  shell/built-in.o  sysklogd/built-in.o  
	util-linux/built-in.o  util-linux/volume_id/built-in.o
```



# gen_build_files.sh分析

这里生成了一些文件。

Kbuild是这里生成的，根据Kbuild.src来生成。

```
include/applets.h
generated from applets.src.h
include/usage.h
generated from usage.src.h 
```

这个sed命令的效果是这样。

```
hlxiong@hlxiong-VirtualBox:~/work/mylinuxlab/busybox/busybox-1.29.3$ export srctree=`pwd`
hlxiong@hlxiong-VirtualBox:~/work/mylinuxlab/busybox/busybox-1.29.3$ echo $srctree 
/home/hlxiong/work/mylinuxlab/busybox/busybox-1.29.3
hlxiong@hlxiong-VirtualBox:~/work/mylinuxlab/busybox/busybox-1.29.3$ sed -n 's@^//applet:@@p' "$srctree"/*/*.c "$srctree"/*/*/*.c
IF_AR(APPLET(ar, BB_DIR_USR_BIN, BB_SUID_DROP))
IF_UNCOMPRESS(APPLET(uncompress, BB_DIR_BIN, BB_SUID_DROP))
IF_GUNZIP(APPLET(gunzip, BB_DIR_BIN, BB_SUID_DROP))
IF_ZCAT(APPLET_ODDNAME(zcat, gunzip, BB_DIR_BIN, BB_SUID_DROP, zcat))
```



因为在每个文件里，注释格式都是统一的。这3部分信息都要提取出来。

```
//applet:IF_TIME(APPLET(time, BB_DIR_USR_BIN, BB_SUID_DROP))

//kbuild:lib-$(CONFIG_TIME) += time.o

//usage:#define time_trivial_usage
//usage:       "[-vpa] [-o FILE] PROG ARGS"
//usage:#define time_full_usage "\n\n"
//usage:       "Run PROG, display resource usage when it exits\n"
//usage:     "\n	-v	Verbose"
//usage:     "\n	-p	POSIX output format"
//usage:     "\n	-f FMT	Custom format"
//usage:     "\n	-o FILE	Write result to FILE"
//usage:     "\n	-a	Append (else overwrite)"
```





```
$(MAKE) $(build)=applets
```

```
$(build)是-f scripts/Makefile.build obj
```

所以展开就是：

```
make -f scripts/Makefile.build obj=applets
```

所以需要先看一下Makefile.build文件。

