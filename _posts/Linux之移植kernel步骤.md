---
title: Linux之移植kernel步骤
date: 2017-08-15 23:18:26
tags:

	- Linux

---

内核启动的首先运行的是head.s和head-common.s的内容，然后是main.c的内容。

head.s在目录arch/arm/kernel下。

打开这个文件，可以看到注释里写着是32位arm cpu通用startup代码。

启动代码head.s与kernel被链接到的位置无关。

R0传递的是0，R1传递的是机器码（机器码在arch/arm/tools/mach-types文件里），R2传递的atags的位置。

