---
title: gnome之dconf
date: 2019-07-26 14:07:19
tags:
	- gnome

---



gconf和dconf都是gnome下的配置工具。

gconf是基于xml文件，dconf是基于二进制数据。

所以dconf的效率高一些。现在在逐步取代gconf。

底层都是基于glib的GSettings结构体。

gconf是gnome2里的，dconf是gnome3里面的。



参考资料

1、gconf和dconf有什么区别？

http://www.kbase101.com/question/7753.html