---
title: webhook研究
date: 2021-05-03 08:45:11
tags:
	- webhook

---

--

最近看pushplus、微信企业版这些通知机制，经常看到webhook这个名词。所以研究一下。



webhook首先是一个概念，而不是某一个具体的东西。

从名字上看，我们也知道就是一个回调机制。

简单来说，webhook就是一个接受http post/get的url。

一个实现了webhook的api提供商，就是在事件发生的时候，向这个配置的url发送一条消息。



主要用途就是更新客户端，发送实时消息。



参考资料

1、webhook功能概述

https://www.cnblogs.com/zhihuifan10/p/11114816.html