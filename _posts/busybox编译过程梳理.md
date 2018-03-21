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
