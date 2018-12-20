---
title: btstack（4）代码阅读
date: 2018-12-20 15:18:35
tags:
	- 蓝牙
---



我觉得奇怪，为什么avdtp的直接调用了l2cap_send函数呢？

这样怎么体现分层呢？

各个层都看到有对L2CAP的函数的调用。

