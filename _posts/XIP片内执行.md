---
title: XIP片内执行
date: 2020-06-29 11:29:51
tags:
	- 嵌入式

---

1

xip是eXecute In Place的缩写。

表示的是这样的行为：

代码在一个spi的nor flash里直接执行，而不需要拷贝到ram里执行。

nor flash的存储空间被映射到soc的内存空间。被当成一块内存来看待。

xip的典型用法是作为bootloader。

XIP代码一般是比较短小的，用来执行一些基础的初始化行为，例如初始化ram，然后把后面的代码拷贝到内存里执行。

要使用xip功能，需要满足2个基本条件：

1、nor flash必须支持xip 模式。

2、soc的spi控制器必须支持xip模式。



xip模式只支持读操作。



参考资料

1、NOR Flash XIP

https://doc.micrium.com/display/TECHOV/NOR+Flash+XIP