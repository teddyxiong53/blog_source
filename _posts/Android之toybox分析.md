---
title: Android之toybox分析
date: 2020-04-16 17:38:01
tags:

	- Linux

---

1

android为什么选择toybox呢？

toybox跟busybox有哪些区别？

在Android5.0之前，还有了一个toolbox。这个选择已经废弃了，被toybox替换了。



bin、xbin、sbin的区别

xbin下面放的是extra的工具，例如你自己编译busybox的，就放在xbin目录下，这样就不会覆盖默认的ls、cat这些基础工具。



toybox的代码在aosp/external/toybox目录下。



为了方便分析，我在Ubuntu上编译运行toybox看看。



从这里https://github.com/landley/toybox下载代码。

```
make defconfig # 什么都不改，只是为了生成.config文件。
make -j4
```

当前不能编译过。是lsattr有问题。我把这个屏蔽掉。用make menuconfig去掉这个命令的编译。

再编译就可以了。

生成的toybox在generated/unstripped目录下。

为了方便调试。

修改Makefile里，加上：

```
CFLAGS += -g -O0
```



代码分析

入口文件是main.c。

toys.h

```
#include "generated/config.h"
	这个就是包括了CONFIG宏。
#include "lib/portability.h"
	这个就是可移植性。
#include "lib/lib.h"
	这个定义了一些工具函数。
#include "lib/lsm.h"
	几个函数声明。
#include "lib/toyflags.h"
	几个宏定义。
#include "generated/newtoys.h"
	这个就是生成的所有命令对应的函数声明。
#include "generated/flags.h"
	这个就是每个命令的参数。
#include "generated/globals.h"
	这个是每个命令的数据结构体。
	最后用一个union，把所有的结构体包起来。
	这个就跟busybox里的，用一个全局数组来存放，有异曲同工之妙。
	不过看起来更加好理解一些。
#include "generated/tags.h"
	一些宏定义。
struct toy_context toys;
union global_union this;
	表示命令的上下文。
char toybuf[4096], libbuf[4096];
	2个大的是数组。
	
```



参考资料

1、

https://blog.csdn.net/ly890700/article/details/72615465