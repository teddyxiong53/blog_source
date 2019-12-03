---
title: Linux内核之ARM正式页表和临时页表
date: 2018-03-18 11:11:46
tags:
---

1

Linux在启动之初会建立临时页表，但是在start_kerne函数中setup_arch又会建立正真的页表和页目录。

临时页表建立的空间和正式页表建立的空间分别部署于不同的空间，因此不会出现覆盖或者修改等现象。

arm linux使用两级页表，L1是pgd，L2是pte。

其中L1页表共2048项，每项占用8bytes，每项对应2M内存，共占用2048*8=16K bytes。

arch/arm/include/asm/pgtable-2level.h



参考资料

1、ARM-Linux （临时，正式） 建立页表的比较

https://blog.csdn.net/edwardlulinux/article/details/38967521

2、arm linux 临时页表的建立

https://blog.csdn.net/flaoter/article/details/73381695