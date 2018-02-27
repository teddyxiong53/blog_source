---
title: flash知识梳理
date: 2018-02-27 20:09:23
tags:
	- flash

---



nor flash：

像访问SDRAM一样，所以可以片内执行。

读时序类似与SDRAM。

可以用来存放代码。

nand flash：

不能片内执行。地址线宽度不确定，是8位、16位或者32位。

主要用来存放数据。U盘的内部就是nand flash。



spi flash则是外挂的flash，不是在芯片的寻址空间里。

优点是便宜。

缺点是速度较慢。

这种spi接口的flash也可以作为mtd设备。



并口flash和串口flash。

对于nor flash而言，CFI接口 = JEDEC接口= 并行接口。



对于S3C2410平台而言，外接的nor flash直接映射在CPU的内存空间上，可以直接用通用的drivers/mtd/maps/physmap.c的驱动。

驱动开发者需要做的事情就是在bsp文件里，配置一下resource。

