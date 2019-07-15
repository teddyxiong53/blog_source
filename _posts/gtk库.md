---
title: gtk库
date: 2018-11-12 13:38:19
tags:
	- Linux

---



gtk是GNOME的基础库。

xfce也可以在gtk上跑起来。

```
CFLAGS+=`pkg-config --cflags --libs  gtk+-2.0`
```

注意是gtk+-2.0 ，那个加号不要缺了。不然找不到的。



参考资料

1、ubuntu安装GTK2.0

https://blog.csdn.net/goodluckwhh/article/details/39992803





