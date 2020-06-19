---
title: 蓝牙之GATT
date: 2018-12-13 16:33:35
tags:
	- 蓝牙

---

1

```
我的理解：
是不是可以把GAP理解为tcpip协议的IP层。
GATT理解为UDP层。
GATT的各种service的UUID，就相当于udp端口号。

我觉得这个是可以帮助理解的。
GATT的确扮演的是传输层的角色。
```



看ble，就看到GATT这个东西，GATT和ble是什么关系？

什么是GATT？

**GATT是在蓝牙连接的基础上，收发很短小的数据段的规范。**这些短小的数据段，被称为属性（Attribute）。

要讨论GATT，需要先看看GAP的概念。

**GAP是所有蓝牙设备都必须有的。**

**GATT是ble设备特有的。**

GATT有服务端和客户端这2种角色。

ATT协议为所有基于ble link的应用提供了一个底层的框架。

ATT协议对应GATT profile。

GATT profile定义地更加具体。

1、一组通用的att类型。例如primary service（基础服务）、secondary service（二级服务）。

# GATT和ATT是什么关系？

蓝牙4.0引入了2个核心协议：GATT和ATT。

GATT是Generic ATTribute protocol。

ATT是ATTribute protocol。

GATT基于ATT。

**所有的ble profile一定是基于GATT。**

也就是说所有的ble服务都是用**ATT作为应用协议。**

GATT 就是使用了 ATT（Attribute Protocol）协议，ATT 协议把 Service, Characteristic遗迹对应的数据保存在一个查找表中，查找表使用 16 bit ID 作为每一项的索引。

一旦两个设备建立起了连接，GATT 就开始起作用了，这也意味着，你必需完成前面的 GAP 协议。这里需要说明的是，GATT 连接，必需先经过 GAP 协议。

GATT 连接需要特别注意的是：**GATT 连接是独占的**。也就是一个 BLE 外设同时只能被一个中心设备连接。一旦外设被连接，它就会马上停止广播，这样它就对其他设备不可见了。当设备断开，它又开始广播。



中心设备和外设需要双向通信的话，唯一的方式就是建立 GATT 连接。

GATT 通信的双方是 C/S 关系。外设作为 GATT 服务端（Server），它维持了 ATT 的查找表以及 service 和 characteristic 的定义。中心设备是 GATT 客户端（Client），它向 Server 发起请求。需要注意的是，所有的通信事件，都是由客户端（也叫主设备，Master）发起，并且接收服务端（也叫从设备，Slave）的响应。



Service 是把数据分成一个个的独立逻辑项，它包含一个或者多个 Characteristic。每个 Service 有一个 UUID 唯一标识。 UUID 有 16 bit 的，或者 128 bit 的。**16 bit 的 UUID 是官方通过认证的，需要花钱购买**，128 bit 是自定义的，这个就可以自己随便设置。

在 GATT 事务中的最低界别的是 Characteristic，Characteristic 是最小的逻辑数据单元，当然它可能包含一个组关联的数据，例如加速度计的 X/Y/Z 三轴值。



与 Service 类似，每个 Characteristic 用 16 bit 或者 128 bit 的 UUID 唯一标识。你可以免费使用 Bluetooth SIG 官方定义的[标准 Characteristic](https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicsHome.aspx)，使用官方定义的，可以确保 BLE 的软件和硬件能相互理解。当然，你可以自定义 Characteristic，这样的话，就只有你自己的软件和外设能够相互理解。



实际上，和 BLE 外设打交道，主要是通过 Characteristic。你可以从 Characteristic 读取数据，也可以往 Characteristic 写数据。这样就实现了双向的通信。**所以你可以自己实现一个类似串口（UART）的 Sevice，这个 Service 中包含两个 Characteristic，一个被配置只读的通道（RX），另一个配置为只写的通道（TX）。**



#GAP

GAP是Generic Access Profile的缩写。

**GAP用来控制设备连接和广播。决定了你的设备是否可以跟其他设备交互，以及怎样交互。**

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

**GATT是独占的。ble设备连接后，就停止广播了。其他设备就看不到它了。**





#HRP

以HRP这个为例，心率profile。

文档20页左右。描述还比较简单。

## 配置

定义了2个角色：sensor和collector。

sensor相当于server，collector相当于client。

这个只能在ble传输层上走。





**GATT层是真正传输数据所在的层。**

一个GATT 服务器通过**一个属性表的表格来组织数据。**

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

4、BLE GATT 介绍

https://www.cnblogs.com/smart-mutouren/p/5937990.html

5、Bluetooth GATT Profile Spec 解读

这个非常好。

https://blog.csdn.net/utadalight/article/details/80057032

6、蓝牙低功耗profile：ATT和GATT

https://blog.csdn.net/bxqs001/article/details/37967145

7、BLE协议--ATT、GATT

https://www.jianshu.com/p/d5e65cbb6b73

8、BLE安全入门及实战（1）

蓝牙的安全问题，的确值得关注。

https://www.secpulse.com/archives/75756.html

9、实战智能门锁

https://zhuanlan.zhihu.com/p/30393145

10、Bluetooth: ATT and GATT

https://epxx.co/artigos/bluetooth_gatt.html