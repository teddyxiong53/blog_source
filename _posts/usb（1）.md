---
title: usb（1）
date: 2024-04-02 15:52:17
tags:
	- usb

---

--

# usb otg

USB host 与 OTG有什么区别？

简单的说，如果一个数码设备支持USB HOST，那么它就可以从另外一个USB设备中取得数据。 

USB HOST线可以使得很多智能手机支持连接鼠标、键盘、硬盘、U盘、MP3、USB游戏手柄、USB HUB、USB网卡、USB打印机、手机、USB SIM手机卡读卡器等一堆设备，好处多多

==OTG就是只要设备支持，双方都可以为USB host.==

## 概述

OTG设备使用插头中的ID引脚来区分A/B Device，

ID接地被称作为A-Device,充当USB Host，A-Device始终为总线 提供电力，

ID悬空被称作为B-Device,充当USB Device，

==设备的USB Host/USB Device角色可以通过HNP(主机交换 协议)切换。==

OTG设备连接时不能跨越USB Hub，如果跨越USB Hub则失去HNP功能。

A-Device/B-Device与USB Host/Device没有必然的关系,

主机切换完毕后A-Device变成USB从设备，但是仍然为总线供电。

## SB-OTG插槽类型

As Host Only ：提供标准的A插座，普通的USB Host并带有TPL（支持设备列表)

As Device Only：仅能作为外设的B-Device（分为插头一体和插头线缆分离的）

OTG Dual    ：使用Micro AB插座，可以在运行时切换Host/Device。

OTG Dual  在插头插入后会先打开VBus，如果没有设备连接则关闭VBus，并开启ADP侦测，而EAs Host Only 则 不会再次关闭VBus

## 协议

### SRP（Session Request Protocol）对话请求协议：

SRP协议允许Adevice在总线为使用时通过切断VBUS来节省电源消耗，

任何一类Adevice都应该能够响应SRP请求，任何Bdevice也应该能够发起SRP请求，

### ADP（Attach Detection Protocol）：

提供是否有对端设备插入的检测，支持任何OTG设备

### HNP（Host Negotiation Protocol）主机交换协议：

OTG设备通过HNP来切换Host/Device角色，

Adevice通过查询Bdevice的OTG性能描述符来判断是否支持HNP协议，

以判断Bdevice是否为两用的OTG设备，

如果Bdevice支持HNP协议，Bdevice将会返回有效的OTG性能描述符，随后Adevice产生一个SetFeature命令告知Bdevice：

你可以在总线挂起时以主机的方式工作，Adevice发送了这个SetFeature命令后挂起总线， 本次Session结束后Host回到Adevice手里。



## 设备框架

### OTG描述符

在设备枚举时，A-Device通过GetDeor向B设备请求OTG描述符。

OTG描述符也应当作为GetConfiguration（）的一部分返回。

其中的bmAttributes标示B-Device是否支持ADP/HNP/SRP标准设备特性，

通过SetFeature（）设置。

### b_hnp_enable  

设置此特性，显示B-Device被允许进行HNP，A设备必须在T(HOST_REQ_SUSP)时间内挂起总线，此特性在session结束时清除。

### a_hnp_support

早期OTG版本的兼容特性，设置这个特性指示B-Device对端的A-Device支持HNP。

### a_alt_hnp_support  

该标志已被废弃



## 连接方式（Host -> Device）

### As Host Only 与 仅作为外设的B-device（带A插头型）

Host端检测到A插头插入，停止ADP，打开VBus，因为B-Device的A插头与设备作为一体，此时B-Device必定与A插头连接，Host检测到外设连接，开始枚举。  

### As Host Only 与 仅作为外设的B-device（A插头为线缆连接）

Host段检测到A插头插入，停止ADP，打开VBus，如果B-Device是线缆连接完毕在将A插头插入则整个连接过程与上面无异，因为此 时B-Device可能还没有插入插头，则设备连接超时，VBus再次关闭，等待下一次ADP的改变（线缆连接完毕），再次打开VBus，此时开始正常总 线枚举。

### OTG Device 与 OTG Device

Host端检测到插头插入，则打开VBus，如果没有外设检测到，则关闭VBus，打开ADP Probing，Device端检测到插头插入，则打开SRP，如果线缆没有插入，则SRP超时，Device端开始进行ADP Probing，当线缆连接完毕，Device端侦测到ADP变化，发送SRP请求Host打开VBus，Host回应SRP并且打开VBus，完成设备连接。

# otg问题解决

https://blog.51cto.com/u_15315240/5109960

# android usb代码分析

https://www.cnblogs.com/cascle/p/4442787.html

