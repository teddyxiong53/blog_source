---
title: gui之cairo
date: 2021-06-02 10:40:11
tags:
	- gui

---

--

cairo 是一个免费的矢量绘图软件库，它可以绘制多种输出格式。

Linux 绘图可以通过 X Window 系统、Quartz、图像缓冲格式或 OpenGL 上下文来实现。

另外，cairo 还支持生成 PostScript 或 PDF 输出，从而产生高质量的打印结果。

在理想情况下，cairo 的用户可以在打印机和屏幕上获得非常接近的输出效果。

cairo 的一项主要设计目标是提供尽可能接近的输出。

**这种一致的输出使 cairo 非常适合 GUI 工具集编程和跨平台应用程序开发。**

使用同一个绘图库打印高分辨率的屏幕和绘制屏幕内容，这种功能具有显著的优点。



cairo 是用 C 编写的，但是为大多数常用的语言提供了绑定。

选用 C 语言有助于创建新的绑定，同时在进行 C 语言调用时可以提供高性能。

应该特别注意 Python 绑定，它支持快速原型开发，而且降低了学习 cairo 绘图 API 的门槛。



cairo 是一个**矢量绘图（vector drawing）**库，

因此绘图需**要对图形进行几何描述**，而不是描述位图中填充的像素。

在采用**位图绘图（bitmap drawing）**时，按照预先决定的布局用预先决定的颜色填充一系列像素，而且图形的质量与位图的大小成正比。



许多有影响力的开放源码项目已经采用了 cairo，cairo 已经成为 Linux 图形领域的重要软件。已经采用 cairo 的重要项目包括：

- Gtk+，一个广受喜爱的跨平台图形工具集
- Pango，一个用于布置和呈现文本的免费软件库，它主要用于实现国际化
- Gnome，一个免费的桌面环境
- Mozilla，一个跨平台的 Web 浏览器基础结构，Firefox 就是在这个基础结构上构建的
- OpenOffice.org，一个可以与 Microsoft Office 匹敌的免费办公套件



Linux的两大流行桌面环境KDE和Gnome，其对应的基础组件是QT和GTK+，

相对于框架性质的QT，GTK+则依然保持着自由与开放的传统，

从底层绘图到上层程序库都由其他开源库组成，

cairo就是GTK+采用的底层图形库，负责构建图形界面。



HelloWorld

从awtk的代码的3rd目录下的cairo的demo目录下，找到一个stars.c文件。编译。

```
 gcc stars.c `pkg-config --libs --cflags cairo` 
```

运行不报错。但是也没有看到效果。

我就看看用到了哪些接口吧。

最新版本是1.16的。



功能分为3个部分：

drawing

```
cairo_t — The cairo drawing context
```



fonts

surfaces



struct _cairo_backend

可以对接多种后端，只要后端实现这个结构体的接口就行了。

```
typedef enum _cairo_backend_type {
    CAIRO_TYPE_DEFAULT,
    CAIRO_TYPE_SKIA,//这个是什么？
} cairo_backend_type_t;
```

创建一个上下文。

```
cr = cairo_create (surface);
```

搜索一下awtk里哪些地方用到这个接口了。

在vgcanvas里用到了。

lcd_nanovg_init

参考资料

1、用 cairo 实现跨平台图形

https://www.cnblogs.com/cnland/archive/2013/01/16/2862422.html

2、官方手册

https://www.cairographics.org/manual/