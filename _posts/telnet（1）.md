---
title: telnet（1）
date: 2018-08-10 22:37:01
tags:
	- 网络

---



telnet协议是tcpip协议族里的一员。是Internet远程登录服务的标准协议。

telnet协议的目的是提供一种相对通用的、双向的、面向8bit字节的通信方法。

telnet的特点：

1、适应异构。

为了适应异构，定义了NVT（Net Virtual Terminal）。作为中间数据。

2、传送远端命令。

ascii码包括95个可打印字符和33个控制字符。

当用户输入控制字符时，NVT把它转换为特殊的可打印字符在网络上传送。到达远端后再转换回来。

3、数据流向。

4、强制命令。

这个是借助于tcp的urgent数据来实现的。

5、选项协商。



# 原理

telnet协议的三大组成部分：

1、NVT .

2、操作协商定义。

3、协商有限状态机。



# 参考资料

1、Telnet协议详解

https://www.cnblogs.com/liang-ling/p/5833489.html