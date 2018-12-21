---
title: btstack之log分析方法
date: 2018-12-21 14:12:35
tags:
	- 蓝牙
---



我开始还觉得奇怪，btstack的日志怎么看不到呢？原来是在/tmp/pklg里。这个是可以用wireshark打开的包格式。把文件用wireshark打开就好了。

协议是PKGLOG的。

这个记录日志的方式，确实让我开了眼界。这个方式很好，可以看到协议包的内容。


















