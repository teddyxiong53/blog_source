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



# 经典蓝牙的gap和ble的gap

经典蓝牙（BR/EDR）的GAP（Generic Access Profile）和BLE（Bluetooth Low Energy）的GAP在概念上类似，但在具体功能和实现上有一些差异。以下是它们的关系和区别：

| **特性**     | **经典蓝牙的GAP**                         | **BLE的GAP**                                    |
| ------------ | ----------------------------------------- | ----------------------------------------------- |
| **协议层**   | Bluetooth BR/EDR协议栈的一部分            | Bluetooth Low Energy协议栈的一部分              |
| **主要功能** | 定义设备如何发现、连接和交互              | 定义设备如何发现、连接和交互                    |
| **发现过程** | 通过查询设备和名称解析等方式              | 通过广播和扫描等方式                            |
| **连接过程** | 使用连接请求和连接确认等机制              | 使用连接请求和连接事件等机制                    |
| **角色**     | 支持主设备（Master）和从设备（Slave）角色 | 支持主设备（Central）和从设备（Peripheral）角色 |
| **安全性**   | 支持配对和绑定、加密等功能                | 支持配对和绑定、加密等功能，并有更多的安全特性  |
| **应用场景** | 音频设备、手机配件、文件传输等            | 物联网设备、传感器、智能家居、健康监测设备等    |
| **引入版本** | Bluetooth 1.0                             | Bluetooth 4.0                                   |

### 关系与区别

- **关系**：
  - **基本概念相同**：GAP在经典蓝牙和BLE中都扮演着相似的角色，即定义设备如何被发现、如何建立连接以及如何互操作。
  - **协议结构相似**：两者都处于蓝牙协议栈的上层，负责定义设备的访问和连接模式。

- **区别**：
  - **发现和连接机制**：经典蓝牙的设备发现过程依赖于查询和名称解析，而BLE则使用广播和扫描机制进行设备发现。BLE的GAP支持广播（Advertising）和扫描（Scanning）两种操作。
  - **角色名称与功能**：经典蓝牙中使用主设备和从设备的概念，而BLE中则使用中央设备（Central）和外围设备（Peripheral）。虽然名称不同，功能类似，但BLE中的角色更注重低功耗特性。
  - **安全性增强**：BLE在安全性方面引入了更多的特性，如保护隐私地址、LE Secure Connections等，以应对更广泛的物联网应用场景。
  - **应用场景和优化**：经典蓝牙的GAP优化用于高带宽应用如音频传输，而BLE的GAP则针对低功耗、低带宽的应用进行优化。

### 总结

经典蓝牙的GAP和BLE的GAP在基本功能上类似，都负责设备发现、连接和交互，但在具体实现、角色分配和安全特性上有所不同。经典蓝牙更适合高带宽应用，而BLE则优化用于低功耗和低带宽的应用场景。

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