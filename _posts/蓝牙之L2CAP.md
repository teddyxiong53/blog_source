---
title: 蓝牙之L2CAP
date: 2018-12-11 20:53:44
tags:
	- 蓝牙

---



L2CAP是Logic Link Control Adapter Protocol。

逻辑链路控制和适配协议。

用来支持上层协议的多路复用、数据分段和重组、质量服务。



L2CAP的主要功能

# 协议复用

基带协议不支持任何类型域。

L2CAP必须能够区分高层协议。例如：服务搜索协议、RFCOMM。

# 分段和重组

跟有线通信相比，由基带协议定义的分组在大小上收到限制。



# 参考资料

1、蓝牙核心-L2CAP

https://blog.csdn.net/u010657219/article/details/42105193