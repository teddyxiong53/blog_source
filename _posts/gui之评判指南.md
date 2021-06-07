---
title: gui之评判指南
date: 2021-06-02 10:07:11
tags:
	- gui

---

--

看看当前在qemu里运行的qt，依赖了哪些图形相关的库，分别又是起什么作用。

libdrm是做什么的？

vexpress 图形加速有什么硬件？



https://qemu-project.gitlab.io/qemu/system/arm/vexpress.html

PL111 LCD display controller



https://www.kernel.org/doc/html/v4.14/gpu/pl111.html

The PL111 is a simple LCD controller that can support TFT and STN displays.



参考资料

1、这个开源的6千行UI框架，能打败QT，MFC吗？

这个高赞回答提的很多问题，值得思考。

https://www.zhihu.com/question/66934513/answer/248036488

2、GUI 引擎评价指标

主要就是总结这篇文章的。

https://github.com/zlgopen/gui-lib-evaluation