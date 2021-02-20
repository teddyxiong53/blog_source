---
title: 蓝牙之arm平台移植bluez
date: 2018-11-27 16:47:35
tags:
	- 蓝牙

---



bluez作为当前最成熟的开源蓝牙协议栈，从内核2.4.6版本开始已经成为内核的一部分。

对于桌面环境，bluez默认已经是好的了。

但是对于嵌入式arm，我们还是需要自己来移植。

就是需要交叉编译几个依赖库。

现在不用管移植了。buildroot里默认就可以编译好。



参考资料

1、ARM平台上蓝牙协议栈Bluez的移植使用和配置

https://blog.csdn.net/gatieme/article/details/48751743