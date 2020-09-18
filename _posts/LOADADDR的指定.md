---
title: LOADADDR的指定
date: 2017-05-07 19:06:04
tags:

	- uboot

	- linux

---

编译kernel的uImage的时候，提示了LOADADDR没有指定的错误。

为什么编译uImage要指定LOADADDR，为什么一般看到是0x80008000？
LOADADDR是给uboot用的，前面要预留32K的空间。
uboot传递给kernel的参数在内存最前面的位置往后偏移0x100字节的位置。
在kernel的Documents目录下有Booting文件，有提到这个。

