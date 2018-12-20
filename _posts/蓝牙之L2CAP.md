---
title: 蓝牙之L2CAP
date: 2018-12-11 20:53:44
tags:
	- 蓝牙
typora-root-url: ..\
---



L2CAP是Logic Link Control Adapter Protocol。

逻辑链路控制和适配协议。

用来支持上层协议的多路复用、数据分段和重组、质量服务。



![](/images/L2CAP在协议栈里的位置.png)

由上面的图可以得到这些信息：

1、L2CAP在ACL之上。可以传控制信息。是异步的。

2、L2CAP是协议栈里的重要中枢。



L2CAP负责包的分片和重组。



包头是这样：

```
len(2 bytes)| chn id(2 bytes) | payload |
```

chn id可能取值：

0：无效。

1：signal 通道。

2：无连接通道。

3：AMP管理协议。

4到0x3e：保留。

0x3f：AMP测试管理。

0x40到0xffff：动态分配。



# 模式

有两种模式：

1、SM模式。Streaming Mode。

2、ERTM模式。增强重传模式。

# L2CAP提供的功能

1、协议和信道的复用。

2、分片和重组。

3、质量服务。

基带协议不支持任何类型域。

L2CAP必须能够区分高层协议。例如：服务搜索协议、RFCOMM。

跟有线通信相比，由基带协议定义的分组在大小上收到限制。

# L2CAP组成

1、通道管理。

2、资源管理。

L2CAP只支持ACL。不支持SCO。



# 参考资料

1、蓝牙核心-L2CAP

https://blog.csdn.net/u010657219/article/details/42105193

2、蓝牙L2CAP剖析（一）

https://blog.csdn.net/XiaoXiaoPengBo/article/details/51364483

3、Bluetooth L2CAP介绍

https://www.cnblogs.com/hzl6255/p/3801732.html