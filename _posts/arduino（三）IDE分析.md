---
title: arduino（三）IDE分析
date: 2018-04-16 14:14:58
tags:
	- arduino
typora-root-url: ..\
---



arduino的IDE也是开源的。

源代码在这里：https://github.com/arduino/Arduino/

下载下来，是一个eclipse工程，用eclipse打开看看。

![](/images/arduino（三）IDE分析.png)

但是这个跑不起来。

是基于Swing写的。

入口是这里：

错误: 找不到或无法加载主类 processing.app.Base

