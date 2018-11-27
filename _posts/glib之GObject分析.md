---
title: glib之GObject分析
date: 2018-11-27 09:26:24
tags:
	- glib

---



大多数现代计算机语言都带有自己的类型和对象系统，并附带算法结构。

GObject对象系统提供了一种灵活的、可扩展的、容易映射的（到其他语言）的面向对象C语言框架。

它的实质可以概括为：

1、一个通用类型系统。

2、一个基本类型的实现集。

3、一个信号系统。



GObject 是基于GType的。

GType是glib运行时类型认证和管理系统。

理解GType是理解GObject的关键。



在GObject系统里，对象由三部分组成。

1、对象的id标识。

2、对象的类结构。

3、对象的实例。





参考资料

1、GObject对象系统

https://www.ibm.com/developerworks/cn/linux/l-gobject/

