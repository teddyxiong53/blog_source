---
title: gui之opengl
date: 2021-05-28 14:44:11
tags:
	- gui

---

--

opengl是用于渲染2D、3D矢量图形的跨语言、跨平台的应用程序编程接口（API）。

这个接口由近350个不同的函数调用组成，

用来绘制从简单的图形比特到复杂的三维景象。

而另一种程序接口系统是仅用于Microsoft Windows上的Direct3D。

OpenGL常用于CAD、虚拟现实、科学可视化程序和电子游戏开发。



OpenGL的高效实现（利用了图形加速硬件）存在于Windows，部分UNIX平台和Mac OS。

这些实现一般由显示设备厂商提供，而且非常依赖于该厂商提供的硬件。

**开放源代码库Mesa是一个纯基于软件的图形API，它的代码兼容于OpenGL。**

但是，由于许可证的原因，它只声称是一个“非常相似”的API。

OpenGL普及的部分原因是其高质量的官方文件。

OpenGL架构评审委员会随规范一同发布了一系列包含API变化更新的手册。

这些手册因其封面颜色而众所周知。



# qt和opengl关系

OpenGL是绘制三维图形的标准API。

Qt应用程序可以使用QtOpenGL模块绘制三维图形，该模块依赖于系统的OpenGL库。

Qt OpenGL模块提供QGLWidget类，可以通过对它子类化，

并使用OpenGL命令开发出自己的窗口部件。对许多三维应用程序来说，这就足够了。

opengl和dx是显卡的接口，最底层的绘图api。

qt是跨平台gui库。

opengl关心的是渲染等，而qt关心的是按钮被点击后引发什么动作之类的。



# opengl和sdl关系

SDL 做的工作就是用X11创建窗口，用EGL创建Surface并绑定，最后就可以用OpenGL或者GLES去render.

# 参考资料

1、OpenGL

https://baike.baidu.com/item/OpenGL/238984?fr=aladdin

2、三维绘图之OpenGL和Qt的结合

https://blog.csdn.net/explore_world/article/details/61919269

3、SDL 和 OpenGL 关系

https://blog.csdn.net/sunny04/article/details/18040035