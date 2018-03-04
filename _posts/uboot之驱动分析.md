---
title: uboot之驱动分析
date: 2018-03-04 15:48:13
tags:
	- uboot

---



uboot也引入了驱动模型的概念。跟kernel的类似，但是又有所区别。

文档在uboot/doc/driver-model/README.txt里。

uboot提供了一个sandbox的配置，方便进行测试：

```
make sandbox_defconfig
make
./u-boot -d u-boot.dtb
退出的方法是输入reset。
```



以enc28j60为例，分析uboot下的驱动写法。

2个文件夹，enc28j60.h和enc28j60.c。

头文件里就定义了寄存器。没有结构体和接口。

