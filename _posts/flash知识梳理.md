---
title: flash知识梳理
date: 2018-02-27 20:09:23
tags:
	- flash

---

1

# nand flash

相比与nor flash，nand flash的一个缺点是容易产生坏块。

因此在使用nand flash的时候，需要使用校验算法来发现并标注坏块。

nand  flash没有地址和数据总线。

nand flash以page为单位进行读写，以block为单位进行擦除。

坏块是指block。

page内部有分为2个区：

main和spare。

main就是存放数据。

spare存放附加信息。例如坏块标记、块的逻辑地址、ECC校验和。



因为nand flash的工艺限制，在nand flash的生产和使用过程中，会产生坏块。

坏块的特性是：在擦除和写入的时候，不能将某些位拉高。



坏块可以分为两种：

1、固有坏块。生产过程中产生的，厂家会在坏块block的第一个page的spare区的第六个bit进行标记。

2、使用坏块。



坏块有可能是假坏块。



mini2440上使用的nand flash是256MB。

page是2K+64.

block是128K+4K。



# nor flash

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

# nand和nor对比

nor的特点：

1、贵。

2、慢。

3、可靠。

所以nor一般用来保存关键数据。

nand的特点：

1、偏移。

2、快。

3、不太可靠。

所以nand一般用来保存大容量的数据。



# OneNand是什么

是三星推出的一种存储技术。是一种混合存储器。

基础概念是把Nand Flash、SRAM芯片和逻辑芯片继承为一颗单芯片。采用的是Nor Flash接口。

所以集合了Nand的高容量和Nor的读取速度快优点于一身。其中的SRAM是作为高速缓存。

因为集成的SRAM是1K，所以OneNand在最前面的1K，是具有片内执行的能力的。







# 参考资料

1、

https://www.cnblogs.com/lifexy/p/7737174.html

2、mini2440硬件篇之Nand Flash

https://blog.csdn.net/hyq458941968/article/details/45269799