---
title: qt之paintengine分析
date: 2021-08-05 11:24:33
tags:
	- qt

---

--

下面对于QT的绘制系统做一个简要说明， 这个系统主要由三部分组成，

- QPainter

- QPaintDevice

- QPaintEngine

  QPainter 是一个绘制接口类，提供绘制各种面向用户的命令。就是画笔。
  QPaintDevice 是一个QPainter绘制的目的地，相当于画布
  QPaintEngine 是基本绘制命令的具体实现。

我们打交道比较多的是 QPainter , 也就是画笔。

注意对于Windows平台来说，

当绘制目标是一个widget的时候，

QPainter只能在 paintEvent() 里面或者由paintEvent()导致调用的函数里面使用。

对于一支画笔，他应该有哪些功能？它是一支多功能笔，就跟瑞士军刀似的。

```
font() 这支笔可以写出的字体。
brush() 当刷子用。
pen() 当笔用
layoutDirection() 往哪个方向写。
一堆的drawXX函数。
例如画点、画线。画矩形。画椭圆
还可以绘图。
drawPixmap
drawImage
	这两个的效果是一样的。drawPixmap在屏幕上比较快。drawImage在其他设备比较快。
	
```

QPainter 提供了一个枚举 CompositionMode 类型，

用来配置QPainter绘制命令的融合模式。

两个用得最多的是 Source 和 SourceOver，

 Source 模式用来绘制那些不透明的对象，

在这个模式下，source中的每个像素会代替destination中的相应像素。

在SourceOver模式，主要用来绘制透明对象，

在这个模式下，source中的像素不会直接替代destination中的像素，source中的像素会覆盖在destination上



**QT 主要实现的后端绘制技术:**

- Raster(光栅化) -
  这个后端技术，**用纯软件的方法实现渲染**，并且他**总是会渲染到一个QImage。**为了优化性能，这里的渲染只使用下面的格式,其他的格式光栅化的性能都很差。这个渲染引擎也是Windows和QWS上默认的渲染引擎。这个渲染引擎作为默认的图像系统可以运行在任何操作系统和软硬件平台上，在命令行中**通过-graphicssystem raster就可以指定用这个渲染引擎启动QT。**
- OpenGL 2.0(ES) 这个是一个主要的硬件加速的图像后端。这个可以运行在桌面机上，以及所有支持OpenGL 2.0 或者OpenGL/ES 2.0的设备上。这也就意味着绝大部分图形芯片都是支持的。这个引擎通过命令行 -graphicssystem -opengl 启动 QPainter 在绘制 QGLWidget 的时候 使用 这个图形引擎。
- OpenVG - 这个后端技术，主要是实现 Khronos 标准的 2D 图形和 矢量图形。 这个使得QT在支持OpenVG的硬件设备上也是支持的，通过命令行 -graphicsssytem openvg开启。



深入QT的 Painter 可以看到 ，QT的绘制引擎 种类很多，总共有11类绘制引擎。

引擎QT界面库是一个相对底层的库。

我们先看下windows下的这个绘制流程

绘制命令从 Windows 的窗口消息 ，WM_PAINT 和 WM_ERASEBKGND 开始



Qt5中的图形主要是通过命令式QPainter API或Qt的声明性UI语言Qt Quick及其场景图后端来完成的。

Qt5的图形功能还包括对打印以及加载和保存各种图像格式的支持



QPainter提供了将矢量图形、文本和图像绘制到不同面（可理解为画布）或QPaintDevice实例（如QImage、QOpenGlPaintDevice、QWidget和QPrinter）上的API。

**实际的绘图发生在QPaintDevice的QPaintEngine中。**

软件光栅器和OpenGL（ES）2.0后端是两个最重要的QPaintEngine实现。

**光栅绘制引擎是Qt的软件光栅化器，在绘制QImage或QWidget时使用。**

它在OpenGL绘制引擎上的优势在于启用抗锯齿时的高质量，以及完整的功能集。



绘制系统：概述QPainer类和架构。
坐标系统：说明QPainer坐标系的工作原理。
绘制和填充：说明QPainter如何执行矢量形状的填充和大纲绘制。

QPainer最重要的渲染目标是：

QImage：一种与硬件无关的直接像素访问图像表示。QPainer将使用软件光栅器绘制QImage实例。
QPixmap：一种适合在屏幕上显示的图像表示。QPainer将主要使用软件光栅器绘制到QPixmap实例。
QOpenGLPaintDevice：一个要呈现到当前OpenGL 2.0上下文的绘制设备。QPainter将使用硬件加速的OpenGL调用来绘制QopenglPaintDevice实例。
**QBackingStore：顶级窗口的backbuffer。**QPainer将主要使用软件光栅器绘制到QBackingStore实例。
QWidget：用于预qt快速用户界面类的基类。**qpainter将使用qbackingstore呈现小部件。**
QOpenGLWidget：画家也可以在QOpenGLWidget上打开。这是为了方便起见，因为从技术上讲，这与使用QopenGLPaintDevice没有什么不同。
QPainer和相关类是Qt GUI模块的一部分。

QPainter用于执行绘图操作，QPaintDevice是可以使用QPainter绘制的二维空间的抽象，QPainter提供了用于绘制不同类型设备的界面。

**QPaintEngine类由QPainter和QPaintDevice在内部使用，除非应用程序程序员创建自己的设备类型，否则对他们隐藏。**
![img](https://img-blog.csdnimg.cn/20200414092048351.png)





参考资料

1、QT的Paint 系统

https://blog.csdn.net/xuleisdjn/article/details/51435669

2、

https://blog.csdn.net/qq21497936/article/details/105505710