---
title: pci接口
date: 2018-04-18 11:08:17
tags:
	- pci

---



搞嵌入式，一直没怎么接触pci这种接口，现在看网络协议栈，看到pci接口的网卡驱动。我觉得需要把pci接口学习一下了。



# 什么是pci接口？

pci是Peripheral Component Interconnect。外设部件互连标准。

它是目前pc上使用最广泛的接口。几乎所有的主板上都有这种接口。

atx主板上，一般有5到6个。

matx上，一般也有2到3个。

规范是1992年发布的 。

pci是用来取代之前的ISA总线的。

ISA这种并行总线有8为和16位两种模式，时钟频率是8MHz，工作频率是33M/66MHz。

pci接口的设备主要有显卡、网卡、声卡。

pci总线是32为的同步复用总线，地址线和数据线是AD31到AD0 。

# pci总线结构

pci总线是一种树形结构，独立于CPU总线。

可以和CPU总线并行操作。

pci总线上可以挂接pci设备和pci桥。

pci总线上是一个主机，多个从机的结构。



# 参考资料

1、百度百科

https://baike.baidu.com/item/PCI总线/132135