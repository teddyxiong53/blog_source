---
title: qt之webkit网页
date: 2021-06-10 15:17:11
tags:
	- qt

---

--

首先先说说QtWebkit、QtWebEngine、QAxWidget三种方式显示网页的应用场景

QtWebkit：

在Qt5.6以前，都是使用QtWebkit组件，但Qt5.6以后，移除了QtWebkit这个组件

QtWebEngine：

Qt5.6以后的MSVC版本，引进了基于Chromium的浏览器引擎 QtWebEngine

QAxWidget：

Qt5.6以后的mingw版本，由于移除了QtWebkit，mingw版本不能使用QtWebEngine，

因此只能使用QAxWidget控件


参考资料

1、

https://blog.csdn.net/qq_36651243/article/details/93173395

2、

https://blog.csdn.net/qq_25800311/article/details/84979800