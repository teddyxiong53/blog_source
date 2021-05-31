---
title: gui之microwindows
date: 2021-05-28 15:28:11
tags:
	- gui

---

--

Microwindows 是一个著名的开放式源码嵌入式GUI 软件，

目的是把图形视窗环境引入到运行Linux 的小型设备和平台上。

作为X Window 的替代品，

Microwindows可以使用更少的RAM 和文件存储空间（100K-600K）

提供与X Window 相似的功能。

Microwindows 允许设计者轻松加入各种显示设备、鼠标、触摸屏和键盘等。

Microwindows 的可移植性非常好，基本上用 C 语言实现，

只有某些关键代码使用了汇编以提高速度。

Microwindows 支持ARM 芯片。

尽管Microwindows 完全支持Linux，但是它内部的可移植结构是基于一个相对简单的屏幕设备接口，

**可在许多不同的RTOS 和裸机上运行。**

 Microwindows 的图形引擎能够运行在任何支持readpixel， writepixel，drawhorzline, drawvertline 和setpalette 的系统之上。

在底层函数的支持之下，上层实现了位图，字体，光标以及颜色的支持。

系统使用了优化的绘制函数，这样当用户在移动窗口时可以提供更好的响应。

内存图形绘制和移动的实现使得屏幕画图显得很平滑，

这点特别在显示动画、多边形绘制、任意区域填充、剪切时有用。

Microwindows 支持新的Linux 内核帧缓存(FrameBuffer)结构，

目前提供每像素1、2、4、8、16、24 和32 位的支持，

另外还支持彩色显示和灰度显示，

其中彩色显示包括真彩色(每像素15、16 和32 位)和调色板(每像素1， 2， 4 和 8 位)两种模式。

在彩色显示模式下，所有的颜色用RGB 格式给出，

系统再将它转换成与之最相似的可显示颜色，

而在单色模式下中则是转换成不同的灰度级。

Microwindows支持窗口覆盖和子窗口概念、完全的窗口和客户区剪切、比例和固定字体，

还提供了字体和位图文件处理工具。

Microwindows 采用分层设计方法。

在最底层，屏幕，鼠标/触摸屏以及键盘驱动程序提供了对物理设备访问的能力。

在中间层，实现了一个可移植的图形引擎，支持行绘制，区域填充，剪切以及颜色模型等。

在上层，实现多种API 以适应不同的应用环境。



由于Microwindows采用了message的方式驱动UI的显示，

跟miniGUI和WIN32的早期的GUI的消息机制是一样的，

因此，只要掌握了Microwindows，就基本上掌握了MiniGUI。



代码在这里

https://github.com/ghaerr/microwindows

看最近的更新是5个月前，说明还算活跃。

官网：

http://www.microwindows.org/

改名原因：

The Nano-X Window System was previously named Microwindows, but has been renamed due to conflicts with Microsoft's Windows trademark. 

实现了3套api

There are three APIs implemented in the system, an X11 API, a Win32 API and an Xlib-like API. 





参考资料

1、开源GUI-Microwindows简介

https://blog.csdn.net/wavemcu/article/details/29194381