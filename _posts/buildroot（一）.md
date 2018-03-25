---
title: buildroot（一）
date: 2018-03-25 08:30:56
tags:
	- buildroot

---



写一个系列文章，把buildroot的编译过程梳理一下。

先看顶层Makefile。

```
1、export当前的版本，2012.05 
2、检查make版本，最低要求是3.81
3、不允许在顶层make -j
4、定义TOPDIR
5、配置文件是Config.in。里面内容结构是跟kconfig一样的。
6、输出目录为output目录。
7、包含.config文件。
8、得到shell的名字。
9、定义工具链。
10、
```

