---
title: Linux的misc device驱动
date: 2017-05-18 23:20:30
tags:

	- Linux驱动

---



misc device是不能明确归类的一些设备，一般都是功能比较简单的设备。Linux给这类设备分配的主设备号是10。

直接看例子，先写一个misc设备的驱动，然后用一个测试程序来测试一下。

设备名为mymisc。

misc device的内部实现就是用字符设备来实现的。



# drivers/misc/eeprom/at24.c

看看这个eeprom的代码。

