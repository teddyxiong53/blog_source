---
title: gstreamer之AppSrc用法
date: 2018-11-19 16:33:28
tags:
	 - gstreamer

---



应用程序有多种方式向pipeline注入数据，而使用AppSrc是最简单的一种方式。

AppSrc有两种工作模式：

1、pull模式。在需要的时候，向应用程序请求数据。

2、push模式。应用程序主动向AppSrc注入数据。





参考资料

1、GStreamer的AppSrc的简单使用

https://blog.csdn.net/coroutines/article/details/43987357