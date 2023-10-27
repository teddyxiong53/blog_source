---
title: Linux内核代码阅读疑问
date: 2018-04-01 22:24:27
tags:
	- Linux内核

---

--

# CONFIG_NO_HZ说明了什么？

在很多的讨论中，都是假定Linux时钟事件是由一个周期时钟提供。

周期性处理很符合人的一般习惯，简单，但是带来了功耗的问题。就算系统无事可做，也必须把系统激活。

为了解决这个问题，内核开发者提出了动态时钟的概念。CONFIG_NO_HZ就是用来激活这个特性的。

https://blog.csdn.net/droidphone/article/details/8112948

这篇文章有详细说明。

