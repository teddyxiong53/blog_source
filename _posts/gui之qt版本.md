---
title: gui之qt版本
date: 2021-05-31 15:37:11
tags:
	- gui

---

--

Qt 一直是在x86、A9、Cotex-A 系列运行，那么既然是单片机，暂时来说也是对硬件环境有高要求的。

- 256 MB 的RAM;
- 500 MHz CPU (推荐1 GHz);
- 支持OpenGL ES 2.0.

QT要想跑在MCU上边，还是需要QT团队做大量移植和简化的工作，然后还要移植Qt Core、Qt GUI、Qt Widgets、Qt QML、Qt Quick Controls 2、Qt Network这些模块，以适应MCU的资源环境，QT还需要C++11编译器的支持，Qt内部使用了大量的POSIX接口函数

总的来说，有两个必要条件：

- 兼容POSIX的操作系统
- 兼容C++11的编译器

现在还加入了MCU的支持，

Qt Quick Ultralite负责GUI主机，

Qt Core作为MCU逻辑部分的开发，使用上C++优秀的面向对象的语言特性，

底层还有个RTEMS开源的实时操作系统，



参考资料

1、

https://zhuanlan.zhihu.com/p/147619105