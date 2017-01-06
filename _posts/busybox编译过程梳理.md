---
title: busybox编译过程梳理
date: 2016-12-20 19:40:12
tags:
	- busybox
---
# 1. 目标之间的依赖关系
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
# 2. 入口位置分析
busybox的执行的入口位置是libbb/appletlib.c的main函数。
我们在这个函数的最前面加上打印：
```
int i=0;
for(i=0;i<argc; i++)
{
    printf("xhl -- argv[%d]:%s \n", i,argv[i]);
}
```
运行效果是这样：
```
populate the dev dir...
 xhl -- argv[0]:/bin/busybox 
 xhl -- argv[1]:mdev 
 xhl -- argv[2]:-s 
drop to shell...
 xhl -- argv[0]:/bin/busybox 
 xhl -- argv[1]:sh 
sh: can't access tty; job control turned off
/ # input: ImExPS/2 Generic Explorer Mouse as /devices/fpga:07/serio1/input/input2

/ # ls
 xhl -- argv[0]:ls 

/ # pwd
/
/ # cc
sh: cc: not found
/ # vi 
 xhl -- argv[0]:vi 
```
可以看到有的命令进入到这个入口了，而pwd却没有进到这个入口。
busybox里的命令分为3种，我们以ls、pwd、arp这3条命令为例进行分析。
```
 IF_LS(APPLET_NOEXEC(ls, ls, BB_DIR_BIN, BB_SUID_DROP, ls))
 IF_PWD(APPLET_NOFORK(pwd, pwd, BB_DIR_BIN, BB_SUID_DROP, pwd))
 IF_ARP(APPLET(arp, BB_DIR_SBIN, BB_SUID_DROP))
```
`APPLET`由busybox创建子进程。
`APPLET_NOEXEC`由fork来创建子进程。
`APPLET_NOFORK`不创建子进程，只调用相关函数，相当于buildin的。效率最高。在linux里fork和exec是很耗时的。
buildin的命令在busybox/shell/ash.c里。
```
static const struct builtincmd builtintab[] = {
	{ BUILTIN_SPEC_REG      "."       , dotcmd     },
	{ BUILTIN_SPEC_REG      ":"       , truecmd    },
```

下面分析一下入口的main函数。
```
{
	1、lbb_prepare。就取得错误码。
	2、从argv[0]得到applet_name。
	3、解析/etc/busybox.conf文件，一般没有这个文件。
	4、run_applet_and_exit(applet_name, argv);
	{
		1、看是否以busybox开头的。是，则执行busybox_main。例如busybox --install -s
		2、find_applet_by_name
		3、run_applet_no_and_exit
	}
}
```
# 3. applet的定义
结构体定义如下：
```
struct bb_applet {
	const char *name;
	const char *main;
	enum bb_install_loc_t install_loc;//命令安装的位置，例如/bin，/sbin等等。
	enum bb_suid_t need_suid;//是否需要root权限。
	unsigned char noexec;
	unsigned char nofork;
};
```

