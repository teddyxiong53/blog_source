---
title: gtk库
date: 2018-11-12 13:38:19
tags:
	- Linux

---



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



参考资料

1、ubuntu安装GTK2.0

https://blog.csdn.net/goodluckwhh/article/details/39992803

2、（一）、一步一步学GTK+之开篇

https://www.cnblogs.com/ikodota/archive/2013/03/08/step_by_step_study_gtk_opening.html



