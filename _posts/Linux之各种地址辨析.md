---
title: Linux之各种地址辨析
date: 2018-03-08 16:24:40
tags:
	- Linux

---



有虚拟地址、线性地址、逻辑地址、物理地址这么4个地址。它们有什么关系。

1、物理地址。这个没有讨论空间，最简单，就是SDRAM的物理地址。硬件决定。

2、逻辑地址。逻辑地址是段偏移地址。C语言里指针，就是一个逻辑地址。在Intel实模式下，逻辑地址和物理地址相等。跟分段有关系。

3、线性地址。线性地址是逻辑地址到物理地址的中间层。逻辑地址加上段基地址就是线性地址。

如果没有分页，线性地址就是物理量地址了。



虚拟地址起始跟上面三个不在一个讨论范围里。

虚拟地址和物理地址一起讨论。



## 虚拟地址物理地址转换函数

1、物理-->虚拟。这个一般用ioremap。

2、虚拟-->物理。这个在应用层做。没有直接的函数，要自己分析proc里的文件才能得到。

https://zhoujianshi.github.io/articles/2017/Linux%20获取虚拟地址对应的物理地址/index.html