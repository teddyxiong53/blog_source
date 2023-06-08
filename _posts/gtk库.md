---
title: gtk库
date: 2018-11-12 13:38:19
tags:
	- Linux

---

--

gtk是GNOME的基础库。一开始gtk是专门为GIMP这个图形处理程序而开发的。因为好用收到欢迎，称为了gnome的基础库。

xfce也可以在gtk上跑起来。

```
CFLAGS+=`pkg-config --cflags --libs  gtk+-2.0`
```

注意是gtk+-2.0 ，那个加号不要缺了。不然找不到的。

gtk依赖了这些库：

```
1、glib。
2、pango。
	这个是实现国际化和本地化的。
3、atk。
	这个是辅助模式。
4、gdk。
	这个是位于x window server和gtk之间的。
5、Cairo。
	图形库。
	
```

安装gtk-3.0的。因为官网教程是基于这个版本。

```
sudo apt-get install libgtk-3-dev 
```

# gtk3和gtk4有什么区别

GTK（GIMP Toolkit）是一种用于创建图形用户界面的开源工具包。GTK 分为不同的主要版本，包括 GTK2、GTK3 和最新的 GTK4。下面是 GTK3 和 GTK4 之间的一些区别：

1. 编程语言支持：GTK3 主要使用 C 语言编写，而 GTK4 引入了更多的语言支持，包括 Rust、Python 和 JavaScript。这使得开发者可以使用自己喜欢的编程语言来编写 GTK4 应用程序。

2. 性能改进：GTK4 引入了许多性能改进，包括更高效的渲染管道和资源管理机制。它采用现代的图形技术，如 Vulkan 和 OpenGL，以提高应用程序的渲染速度和响应性。

3. 硬件加速：GTK4 增加了对硬件加速的支持，利用 GPU 来加速图形渲染。这可以提高应用程序的性能和视觉效果，并使界面更加流畅。

4. 组件重构：GTK4 对许多组件进行了重构和改进。它提供了新的组件，如GtkStackSwitcher和GtkPopover，以及对现有组件的改进，如GtkTreeView和GtkListBox。这些改进提供了更好的可定制性和灵活性。

5. 响应式布局：GTK4 引入了一种新的布局系统，称为 GtkConstraintLayout，它基于约束和关系来实现灵活的自适应界面布局。这使得开发者可以轻松地创建响应式的用户界面，适应不同的屏幕尺寸和设备。

6. 手势和触摸支持：GTK4 提供了更好的手势和触摸支持，使应用程序能够更好地适应触摸屏幕和手势交互。它引入了更多的手势事件和手势识别功能，提供了更直观和现代的触摸体验。

这些是 GTK3 和 GTK4 之间的一些主要区别。GTK4 带来了许多新特性和改进，旨在提供更好的性能、更好的开发体验和更现代化的用户界面。然而，由于 GTK4 相对较新，它的生态系统和工具链可能仍在发展中，因此在选择版本时需要考虑项目的需求和现状。





# 参考资料

1、ubuntu安装GTK2.0

https://blog.csdn.net/goodluckwhh/article/details/39992803

2、（一）、一步一步学GTK+之开篇

https://www.cnblogs.com/ikodota/archive/2013/03/08/step_by_step_study_gtk_opening.html

3、

https://developer.gnome.org/gtk3/stable/gtk-getting-started.html

