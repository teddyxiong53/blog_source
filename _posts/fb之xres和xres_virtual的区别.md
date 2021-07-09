---
title: fb之xres和xres_virtual的区别
date: 2021-07-05 15:43:33
tags:
	- gui

---

--

xres yres是可视区间大小，对应着LCD的显示尺寸。

xres_virtual yres_virtual定义了framebuffer内存中一帧的尺寸。

xres_virtual yres_virtual必定大于或者等于xres yres，可以通过pan操作来显示xres_virtual和yres_virtual定义的显示区域。



参考资料

1、

https://www.cnblogs.com/fah936861121/articles/7105571.html

