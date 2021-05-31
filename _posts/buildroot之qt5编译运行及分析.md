---
title: buildroot之qt5编译运行及分析
date: 2021-05-28 11:03:11
tags:
	- gui

---

--

现在要在嵌入式Linux上跑gui程序。

这一块接触比较少。所以需要先找一个最常见最通用的方案来研究一下。

qt5是buildroot里自带了的。

qt5的整个架构是怎样的？底层依赖了哪些库？

以qemu x86 的，在ubuntu上跑一个gui程序起来。

```
make qemu_x86_64_defconfig
```

这个默认没有选配上qt5的。

还是换一个qemu_arm_vexpress_defconfig

这个之前也用得比较多。只是知道这个是带显示屏的。

这个默认也没有选配qt5.我把c库选成glibc。就可以选配qt5了。

默认只选配了qt5base。

先就这样。

进入QT5选项，勾选gui module 和 widgets module。

而且qt5现在还不可选。

```
*** Qt5 needs host g++ >= 5.0, and a toolchain w/ gcc >= 5.0, wchar, NPTL, C++, dynamic library *** 
```

先看qt5的package里是怎么写的。

下面有这么多的package。

```
qt53d
qt5base
qt5charts
qt5coap
qt5connectivity
qt5declarative
qt5enginio
qt5graphicaleffects
qt5imageformats
qt5knx
qt5location
qt5lottie
qt5.mk
qt5mqtt
qt5multimedia
qt5quickcontrols
qt5quickcontrols2
qt5quicktimeline
qt5remoteobjects
qt5script
qt5scxml
qt5sensors
qt5serialbus
qt5serialport
qt5svg
qt5tools
qt5virtualkeyboard
qt5wayland
qt5webchannel
qt5webengine
qt5webkit
qt5webkit-examples
qt5websockets
qt5webview
qt5x11extras
qt5xmlpatterns
```



比如经典的Qt4系列，当年为满足嵌入式开发提供的Qt/Embedded。

一直以来，对Qt影响比较大的转折点一是2008 Nokia从Trolltech公司收购Qt,二是2012 Aug 09 诺基亚正式放弃该框架。

从这时候起，Qt开始进入5的时代。

技术架构方面有了彻底的变化，主要是**更细粒度的模块化**和重点转向基于opengl的QML、QtQuick技术开发。

这个时候的QML继承了诺基亚的遗产，并且彻底转向以opengl为底层，使得绘图性能更好，

更适合现代图形界面开发。

Qt技术的演变一直以来都是很自然的，符合社会对很多方面的需要，

当然，由于其是一个开源项目，没有了实力资本的支持，

Qt一直以来 很多模块要么缺少功能，要么bug比较多。

**直到目前（2016），Qt5.6系列发布长期支持版本，这才标志着Qt5系列已经相对比较稳定。**

当然，新功能的增加和优化还是会根据需求继续发展。



Qt5开始更加注重模块化，从上层逻辑上分为Qt Essentials、Qt Add-Ons、Technology Preview、商业模块和tools 几部分。



随着需求的不断变化，Qt5新增了很多功能，已经不仅仅是开发界面，而是成为功能丰富的多用途框架。其中一些新功能放进了基础模块，一些以独立的附件模块提供。



Qt自身的属性就是跨平台，即相同功能的api可以在各个平台编译运行。

为了尽可能达到此目的，势必会照顾各平台共有的特性和约束，

**另外一些平台专有的功能以Extras模块提供。**

因为跨平台的特性，所以注定了其在各平台上并不是最优化方案，

一般各平台的原生开发语言和框架在很多方面要优于Qt。



虽然Qt本身是C++，但由于各平台有自己的原生语言，如android，并且上层的api都是通过这些语言导出，虽然Qt可以通过封装的形式调用，但无形中添加了很多步骤，性能上可能会有点折扣。



总体上，现阶段的Qt已经可以满足很多需求，性能和体验上有所提升（当然还有各种缺陷）。

目前，真正的基于操作系统的嵌入设备开发一般会选择改造的android，

由于android系统的完善及应用支持，这方面的优势要远远大于Linux+Qt。

而Qt一般可以用于一些对应用数量要求不多，驱动设备不是很多，

界面需要灵活定制的应用场景，这方面Qt具有一定的优势。



Linux+Qt也是选择之一，另外还可以用嵌入式web服务。



# QML+JS

可以方便快速的开发出高端大气上档次的UI,同时效率又比HTML5高出将近5倍

QML是一种描述性的脚本语言，文件格式以.qml结尾。

语法格式非常像CSS（参考后文具体例子），但又支持javascript形式的编程控制。

QtDesigner可以设计出·ui界面文件，但是不支持和Qt原生C++代码的交互。

QtScript可以和Qt原生代码进行交互，

但是有一个缺点，如果要在脚本中创建一个继承于QObject的图形对象非常不方便，

只能在Qt代码中创建图形对象，然后从QtScript中进行访问。

而QML可以在脚本里创建图形对象，并且支持各种图形特效，以及状态机等，

同时又能跟Qt写的C++代码进行方便的交互，使用起来非常方便。



QML是Qt推出的Qt Quick技术的一部分，是一种新增的简便易学的语言。

QML是一种陈述性语言，用来描述一个程序的用户界面：

无论是什么样子，以及它如何表现。

在QML，一个用户界面被指定为具有属性的对象树。 

这使得Qt更加便于很少或没有编程经验的人使用。





参考资料

1、qml

https://baike.baidu.com/item/QML/153014?fr=aladdin

https://doc.qt.io/qt-5/qtqml-javascript-topic.html

# qt产品线

https://www.qt.io/zh-cn/product/features

```
设计工具
	qt design studio
	qt designer
	qt quick designer
	
开发工具
基础框架
扩展模块

```



# 代码仓库

https://code.qt.io/cgit/qt/qtbase.git/





Qt/e 程序初始化时打开framebuffer，同时将framebuffer的内存映射到自己的空间。有个Qscreen 对象会将上层所有的要显示的东西，放到framebuffer的内存中。linux内核的framebuffer驱动程序控制硬件读取显示。





# 参考资料

1、

https://blog.csdn.net/ansondroider/article/details/114889406

2、buildroot配置QT5和tslib
https://blog.csdn.net/u012577474/article/details/103365647

3、Qt5及模块架构分析

https://blog.csdn.net/yansmile1/article/details/52239746