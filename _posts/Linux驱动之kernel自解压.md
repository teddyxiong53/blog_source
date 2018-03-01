---
title: Linux驱动之kernel自解压
date: 2018-03-01 12:23:18
tags:
	- Linux驱动

---



内核配置项AUTO_ZRELADDR表示自动计算内核解压地址。

我这里使用的soc是bcm2807（bcm2835），他的Makefile.boot内容如下：

zreladdr-y            := 0x00008000

params_phys-y         := 0x00000100

initrd_phys-y        :=0x00800000



总结一下可能的3种情况：

（1）      内核起始地址– 16kB >= 当前镜像结束地址：无需搬移

（2）      内核结束地址 <= wont_overwrite运行地址：无需搬移

（3）      内核起始地址– 16kB < 当前镜像结束地址 && 内核结束地址 > wont_overwrite运行地址：需要搬移