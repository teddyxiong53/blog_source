---
title: Linux显示之tinydrm
date: 2021-12-17 19:14:11
tags:
	- Linux

---

--

drm的，还是会产生fb设备。

有这样的结构体名字：drm_framebuffer

There are 3 MIPI DBI implementation types:

1. Motorola 6800 type parallel bus
2. Intel 8080 type parallel bus
3. SPI type with 3 options:
   1. 9-bit with the Data/Command signal as the ninth bit
   2. Same as above except it's sent as 16 bits
   3. 8-bit with the Data/Command signal as a separate D/CX pin

我当前要调的板子，就属于第三种情况的。



参考资料

1、嵌入式Linux使用TFT屏幕:使用TinyDRM点亮ST7789V屏幕

https://blog.csdn.net/CNflysky/article/details/120492583

2、

https://dri.freedesktop.org/docs/drm/gpu/tinydrm.html