---
title: 蓝牙之GATT
date: 2018-12-13 16:33:35
tags:
	- 蓝牙

---



看ble，就看到GATT这个东西，GATT和ble是什么关系？

什么是GATT？

GATT是在蓝牙连接的基础上，收发很短小的数据段的规范。这些短小的数据段，被称为属性（Attribute）。

要讨论GATT，需要先看看GAP的概念。

GAP是所有蓝牙设备都必须有的。

GATT是ble设备特有的。

GATT有服务端和客户端这2种角色。



#GAP

GAP是Generic Access Profile的缩写。

GAP用来控制设备连接和广播。决定了你的设备是否可以跟其他设备交互，以及怎样交互。

例如Beacon设备，就只能向外发送广播，不支持连接。

## 设备角色

GAP给设备分配了角色，主要就2个：

1、外围设备。例如手环。

2、中心设备。例如手机。

## 广播数据

外围设备通过两种方式向外广播数据：

1、广播数据。Advertising Data Payload。

2、扫描回复。Scan Response Data Payload。

第一种是必须的，因为外围设备必须不停地向外广播，让中心设备知道它存在。

扫描回复是可选的。是由中心设备发起。

广播间隔越长越省电。

# GATT

讨论了GAP之后，我们回到GATT 的主题上来。

GATT可以叫做普通属性协议。

它规定了2个ble设备，通过两种机制进行通信：

1、Service。

2、Characteristic。

一旦2个设备建立了连接，GATT就开始起作用了。

GATT是独占的。ble设备连接后，就停止广播了。其他设备就看不到它了。





#HRP

以HRP这个为例，心率profile。

文档20页左右。描述还比较简单。

## 配置

定义了2个角色：sensor和collector。

sensor相当于server，collector相当于client。

这个只能在ble传输层上走。





GATT层是真正传输数据所在的层。

一个GATT 服务器通过一个属性表的表格来组织数据。

一个属性包括：

1、句柄。属性在GATT表里的索引。

2、uuid（类型）

3、值。



# 参考资料

1、GATT Profile 简介

https://www.race604.com/gatt-profile-intro/

2、gatt官网profile列表

https://www.bluetooth.com/specifications/gatt

3、通用属性配置文件（GATT）及其服务，特性与属性介绍

http://blog.chinaunix.net/uid-21411227-id-5750680.html