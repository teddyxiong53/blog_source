---
title: Linux之gui方案选型
date: 2021-05-26 17:28:11
tags:
	- Linux

---

--

# 概览

```
qt
	收费问题。
	也是比较重量级。
	qt在stm32F4单片机上都可以跑起来了。说明还可以。
gtk
	太重量级，太传统。
tekui
	感觉比较简陋，非主流。
microwindows
	现在改名为nano-x。是轻量级的x11实现。
	可以在电脑进行测试。
	文档写得调理清晰。
	可以先把这个跑一下。
minigui
	还是可以研究一下。
opengui
	可移植性很长。只有x86版本。
	所以不值得看了。
fltk
	对字体支持比较差。
awtk
	zlg公司的。
touchgfx
	现在被stm32公司收购，主推。
	但是只能用在stm32的芯片上。
emwin
	segger公司的。
	ucgui、stemwin都是这个衍生的。
ugfx
GUIslice
GuiLite
LVGL
electron
	这个值得分析一下资源占用情况。需要依赖哪些东西？
	看看在128M+128M的配置下是否跑得起来。
	这种配置跑Android能跑起来吗？最精简的那种。
	可以试一下。
nuklear
	这个是通过在github搜索“gui”，过滤C语言找到的。
	https://github.com/Immediate-Mode-UI/Nuklear
	提供了各种语言的binding。
nanogui
	https://github.com/wjakob/nanogui
然后搜索rtos gui 这样也可以找到另外一些。

```

出现这种现象的根本原因是GUI并不是嵌入式Linux操作系统的内置组件，

嵌入式Linux软件生态中也没有一个轻量级、简单易用、界面美观的GUI系统。

盘点一下常见的嵌入式Linux GUI方案，

Qt/Embedded应该是最容易被提及和选择的选项了，

其它的还有Microwindows、MuniGUI和OpenGUI等，

这些GUI方案都有自己的特点，但也有缺点，

![img](../images/random_name/7920678-e9856e8617b6f79631177599fb43dbd6)



嵌入式产品开发，复杂GUI如何实现一直是一个难题，难倒了不少开发者。由于目前嵌入式产品开发者大多数是电子工程师，很大一部分是从单片机开发技能升级而来，对GUI往往难以把握。

AWTK的出现正是为了解决嵌入式产品GUI开发的这些痛点，在目前取得了很好的成效。

这个是zlg公司开发的。国内的这种通用方案，我不太看好，放弃维护真的只是早晚的事情。

不过可以先看看。

看介绍似乎不错。

采用的是GNU LESSER GENERAL PUBLIC LICENSE协议开源。就是LGPL。

LGPL是GPL的一个为**主要为类库使用设计**的开源协议。

和GPL要求任何使用/修改/衍生之GPL类库的的软件必须采用GPL协议不同。

LGPL允许商业软件通过类库引用(link)方式使用LGPL类库而不需要开源商业软件的代码。

这使得采用LGPL协议的开源代码可以被商业软件作为类库引用并发布和销售。

商用上还好，不强制开源，通过库的方式进行链接。

跑一下看看。

# mingui和microwindows对比

MiniGUI和MicroWindows均为自由软件，

但这两个系统的技术路线却有所不同。

MiniGUI的策略是建立在比较成熟的图形引擎之上，

比如Svgalib和LibGGI，

开发的重点在于窗口系统、图形接口之上。

而MicroWindows的开发重点则在底层的图形引擎之上，

所以可以对裸显示器直接操作，

而窗口系统和图形接口方面的功能还稍有欠缺。

比如说，MiniGUI有一套用来支持多字符集和多编码的函数接口，可以支持各种的字符集，包括GB、BIG5、UNI-CODE等。



Nano-X 的优点 
　　与Xlib实现不同，Nano-X仍在每个客户机上同步运行，这意味着一旦发送了客户机请求包，服务器在为另一个客户机提供服务之前一直等待，直到整个包都到达为止。这使服务器代码非常简单，而运行的速度仍非常快；占用很小的资源。

　　Nano-X 的缺点 
　　1、联网功能部件至今没有经过适当地调整（特别是网络透明性）； 
　　2、还没有太多现成的应用程序可用； 
　　3、没有很多文档说明而且没有很好的支持 
　　4、图形引擎中存在许多低效算法，值得一提的是，该项目的许多控件是从 MiniGUI 中移植过去的，扫雷游戏也是从 MiniGUI 中移植过去的。由于该项目缺乏一个强有力的核心代码维护人员，**2010年Microwindows推出版本0.92后，该项目的发展开始陷于停滞状态。**

# 基于浏览器方案

Dillo -- Dillo是一个小巧（不到300KB），快速，开源多平台的网页浏览器，它完全由C语言编写并基于GTK+库编译而成。Dillo由于它的高效率和对库的依赖性最小，使得它非常适合于嵌入式应用。Dillo可以与一个嵌入式网页服务器配合，就完全可以满足嵌入式窗口管理器的需要。

有没有例子？

代码

https://github.com/dimkr/dillo

看reame里写的，是基于了gtk的。然后兼容性做得并不好。

看起来这个项目并不是一个认真的项目。

# fbui

这个是基于内核来做的。思路值得看一下。

https://github.com/8l/fbui

# 电子相框

https://github.com/NautiluX/slide

这个是在树莓派上可以跑的。基于qt的。

# gui层级划分

目前，在Linux操作系统中，一般可将图形应用库粗略地分为三个不同层次。

第一层次是图形基础设施，它们本身没有提供相应的应用程序编程[接口](https://link.zhihu.com/?target=http%3A//www.hqchip.com/app/1039)，而是集成在操作系统中或采用某种封装形式，用作其他高级图形或者应用程序的基本函数库，较典型的有X Window、SVGALib、f[ram](https://link.zhihu.com/?target=http%3A//www.elecfans.com/tags/ram/)ebuffer（帧缓冲）和LibGGI等;

第二层次是高级函数库，它们提供了大量的应用程序编程接口，较典型的有Xlib、GDK、GTK+、QT、SDL、OpenGL、PEG和DirectFB等;

第三层次多任务窗口系统图形用户界面GUI，较典型的有[Mi](https://link.zhihu.com/?target=https%3A//data.hqchip.com%3A4006/t/8Qa)crowindows、OpenGUI、Qt/Embedded和MiniGUI等。



在低端的嵌入式系统中， 由于用户图形界面仅仅需要用到一些简单的画点、画线、图片显示和中西文输入/显示等，

同时考虑到成本、占资源大小和稳定性等诸多因素，

因此在对Microwindows进行相应裁减的基础上进行应用图形库的设计。

# minigui商用

并且如果使用全志（Allwinner）和瑞芯微（Rockchip）公司的SOC，则可免费获取商业授权，所以MiniGUI是一款值得我们去了解并使用的嵌入式GUI解决方案，支持国产！



# Android最低ram要求

According to an interview with Andy Rubin in 2008 this is the minimum requirements for android:

- 32 MB RAM
- 32 MB Flash Memory
- 200 MHz processor





https://android.stackexchange.com/questions/34958/what-are-the-minimum-hardware-specifications-for-android

# 参考资料

1、

https://elinux.org/User_Interfaces

2、

https://stackoverflow.com/questions/59945182/is-it-possible-to-develop-a-gui-on-linux-embedded-with-just-html-css-and-js

3、

https://www.eet-china.com/mp/a7466.html

4、linux应用项目（一）数码相框（1）数码相框之系统框架

https://blog.csdn.net/fengyuwuzu0519/article/details/72877247

5、

https://blog.csdn.net/fengyuwuzu0519/article/details/72877318

6、

https://www.huaweicloud.com/articles/af46c1b70b0a1f8f3c2396d8ecc157d3.html

7、嵌入式Linux常用GUI系统

https://blog.csdn.net/paladinzh/article/details/96194049

8、嵌入式图形界面

这个罗列了非常多的，很全面。

https://blog.csdn.net/chungle2011/article/details/104880801

9、嵌入式Linux轻量级图形应用库应该如何设计

https://zhuanlan.zhihu.com/p/90983794

10、嵌入式GUI，你真的选对了吗？

https://zhuanlan.zhihu.com/p/62339458

11、盘点嵌入式那些常见的GUI：emWin、TouchGFX、MiniGUI、Qt等

https://blog.csdn.net/ybhuangfugui/article/details/101442421

12、

https://itnext.io/top-five-libraries-for-creating-gui-on-embedded-linux-5ce03903be32

13、Speeding embedded systems time to market using Node.js

https://www.embeddedcomputing.com/technology/software-and-os/speeding-embedded-systems-time-to-market-using-node-js

14、

https://www.cnblogs.com/yangguang-it/p/7237532.html

# 末尾

