---
title: mqtt之mqtt-broker实现之sol
date: 2022-12-12 16:58:17
tags:
	- mqtt

---

--

代码在这里：

https://github.com/codepr/sol

先看readme。

作者写得很清楚，就是模仿mosquitto的行为。

写这个项目的目的是通过实现sol来研究mqtt协议。

支持所有的mqtt v3.1.1（几乎所有）（缺了啥？）

使用epoll作为io多路复用。

开发过程记录在这里：

https://codepr.github.io/posts/sol-mqtt-broker/

作者的信息。

我叫 Andrea Baldan，我是一名软件工程师，目前在我的日常工作中专注于 Python，主要从事物联网软件和云架构。对编程充满热情，尤其是对分布式和并发系统的主题，不断期待提高我的知识。



tutorial这个branch是不一样的。

https://github.com/codepr/sol/tree/tutorial

作者特意写了，不要用于生产环境。

从作者的测试来看，性能是要好于mosquitto。



# 参考资料

1、

