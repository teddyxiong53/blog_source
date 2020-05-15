---
title: 蓝牙之GAP
date: 2018-12-17 13:38:35
tags:
	- 蓝牙
typora-root-url: ../
---



GAP也是一种Profile。

通用访问Profile。

```
1、是最基础的profile。其他的profile都是直接或者间接引用了这个profile。
2、GAP主要是对link layer层的状态进行了抽象，转化成上层的概念。
3、对广播包数据进行封装，使用统一的格式和类型，达到互联的目的。
```

![](/images/蓝牙之GAP在协议栈的位置.png)



**从上面这张图，我们可以看到GAP基本上包括了所有层。**



因此，BLE协议栈定义了一个称作Generic Access（通用访问）的profile，以实现如下功能：
1）定义GAP层的蓝牙设备角色（role）
和3.3中的Link Layer的role类似，只不过GAP层的role更接近用户（可以等同于从用户的角度看到的蓝牙设备的role），包括：
Broadcaster Role，设备正在发送advertising events；
Observer Role，设备正在接收advertising events；
Peripheral Role，设备接受Link Layer连接（对应Link Layer的slave角色）；
Central Role，设备发起Link Layer连接（对应Link Layer的master角色）。

2）定义GAP层的、用于实现各种通信的操作模式（Operational Mode）和过程（Procedures），包括：
Broadcast mode and observation procedure，实现单向的、无连接的通信方式；
Discovery modes and procedures，实现蓝牙设备的发现操作；
Connection modes and procedures，实现蓝牙设备的连接操作；
Bonding modes and procedures，实现蓝牙设备的配对操作。

3）定义User Interface有关的蓝牙参数，包括：
蓝牙地址（Bluetooth Device Address）；
蓝牙名称（Bluetooth Device Name）；
蓝牙的pincode（Bluetooth Passkey）；

蓝牙的class（Class of Device，和发射功率有关）；


用来保证不同的蓝牙设备之间可以相互发现并访问对方。

处理一般业务，如询问、命名、搜索。

处理安全问题，担保。

处理连接相关业务，例如链路建立等。



GAP service，用来表明设备的基本信息的。

```
4种角色
5种状态：
	standby
	advertising
	scanning
	initiating
	connection
	
一个设备可以有多个角色和状态。
```



advertising

```
有两种类型的数据包可以发送，advertising packet和scan Response packet。
它们的大小都是31字节。

ble有40个无线通道，但是广播通道只有3个。
在37M、38M、39M的位置。
选择这3个通道是为了避免跟wifi的通道冲突。

一个设备可以同时进行scan和advertising。

```



在ble下，gap role有四种：

1、broadcaster。发送广播的。

2、observer。接收广播的。

3、外设。接收连接的。

4、中心设备。发起连接的。





# 参考资料

1、GAP

https://baike.baidu.com/item/GAP/7600895

2、[BLE--GAP]GAP Service及其使用

https://blog.csdn.net/suxiang198/article/details/48521335

3、Bluetooth GAP介绍

https://blog.csdn.net/hzl6255/article/details/41930453

4、蓝牙 GAP 最细致的分析上

https://blog.csdn.net/XG_2013/article/details/80864527

5、蓝牙 4.0 中的 GAP Advertising 简介 

https://blog.csdn.net/hongprove/article/details/50903151

6、

https://blog.csdn.net/zwc1725/article/details/80704678