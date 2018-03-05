---
title: 树莓派之dma实验
date: 2018-03-04 22:50:51
tags:
	- 树莓派

---



https://github.com/Wallacoloo/Raspberry-Pi-DMA-Example/blob/master/dma-example.c



思路是用mmap取得dma寄存器的基地址。然后操作。

是直接操作寄存器的。

就是实现dma把一块内存搬移到另外一个内存上的实验。

