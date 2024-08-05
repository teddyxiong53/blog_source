---
title: 蓝牙之L2CAP
date: 2018-12-11 20:53:44
tags:
	- 蓝牙
typora-root-url: ../
---

# 简介

L2CAP是Logic Link Control Adapter Protocol。

逻辑链路控制和适配协议。

重点是逻辑链路。逻辑二字。**它的作用是为2个通信的蓝牙设备提供端到端的通道。**

主要的作用是：

1、协议信道复用。Logical Link是有限的，但要用它来传输数据的上层协议却不止一个（例如ATT和SMP协议），multiplexing便是用过复用的方法来解决这个问题。类似于电脑上IP用同一个，但端口号可以有很多个，不用的应用协议用不同的端口来进行通信。

2、分段与重组。上层的数据可能有很多，但底层设备的处理能力是有限的，分段便是将上层庞大的数据进行切割，让底层方便处理。而重组便是反过来，将底层分散的数据重新组合，传回给上层协议。

3、信道流控。当多个数据流通过不同的逻辑通道流经同一个控制器的时候，每一个通道需要单独的流控制

4、error control。对数据传输出现错误时进行重传，保证数据准确



由于历史发展的原因，

传统蓝牙将数据传输的方式方法抽象为一条条数据链路（data link），

每条链路代表着一种使用着某种传输逻辑（Logic）和传输实体（Physic）的链路。

并由L2CAP进行管理和控制。



OSI 7层模型是通信的基本模型，

蓝牙的协议层次和OSI 7层模型也是可以一一对应的。

蓝牙的LL层和PHY层和OSI模型的数据链路层和物理层基本一一对应，而在LL层之后则区别较大。



首先对于蓝牙这种拓扑结构为最简单的一对一直连应用，

它没有也不需要OSI定义的网络层来为它进行组网和传输路径规划。（不需要网络层）

而到传输层这以块，蓝牙则设计的相对复杂一些。（传输层更加麻烦）

在蓝牙协议中，它主要通过L2CAP协议来共同实现OSI传输层所需求的作用。（L2CAP来实现传输层）



https://www.cnblogs.com/simpleGao/p/17491546.html



# L2CAP在BLE中的实现

L2CAP协议支持很多功能，但BLE用的是简化版本，

和前面说的没太大关系，可以把前面讲的都忘掉。

对于BLE，L2CAP他基本只使用了通道复用（channel multiplexing）功能

# psm

PSM是Protocol Service Multiplexer。协议服务复用。

所谓的multiplexing（多路复用），还是很好理解的：
可用于传输用户数据的逻辑链路只有一条，而L2CAP需要服务的上层Profile和Application的数目，肯定远不止这个数量。因此，需要使用多路复用的手段，将这些用户数据map到有限的链路资源上去。

至于multiplexing的手段，简单又直接（可以说是“协议”的标配）：
1）数据发送时，将用户数据分割为一定长度的数据包（L2CAP Packet Data Units，PDUs），加上一个包含特定“ID”的header后，通过逻辑链路发送出去。
2）数据接收时，从逻辑链路接收数据，解析其中的“ID”，并以此判断需要将数据转发给哪个应用。

这里所说的ID，就是多路复用的手段，L2CAP提供两种复用手段：

1、基于连接的。这个连接不是射频连接，而是逻辑上的L2CAP连接。

CID我可以理解为tcp端口号。

2、无连接的方式。无连接的方式，就没有CID，但是有一个PSM字段。







# 逻辑信道

L2CAP的逻辑信道分配是这样：

ChannelID，缩写为CID。

0x0001：这个信道是作为发送信令的通道。

**0x0002：这个是作为无连接的信道使用。无连接是指没有建立ACL通路。**

0x0040到0xFFFF：这些信道是动态分配的。

==如果是BLE设备，那么0x0005信道是作为BLE的信令通道。而0x0004和0x0006页会被强制分配给BLE，作为ATT和SecurityManager信道。==

这些在btstack的源代码里，都可以看到的。

```
// L2CAP Fixed Channel IDs    
#define L2CAP_CID_SIGNALING                 0x0001
#define L2CAP_CID_CONNECTIONLESS_CHANNEL    0x0002
#define L2CAP_CID_ATTRIBUTE_PROTOCOL        0x0004
#define L2CAP_CID_SIGNALING_LE              0x0005
#define L2CAP_CID_SECURITY_MANAGER_PROTOCOL 0x0006
```



# L2CAP类型

看btstack里：

```
typedef enum {
    L2CAP_CHANNEL_TYPE_CLASSIC,         // Classic Basic or ERTM
    L2CAP_CHANNEL_TYPE_CONNECTIONLESS,  // Classic Connectionless
    L2CAP_CHANNEL_TYPE_CHANNEL_CBM,     // LE
    L2CAP_CHANNEL_TYPE_FIXED_LE,        // LE ATT + SM
    L2CAP_CHANNEL_TYPE_FIXED_CLASSIC,   // Classic SM
    L2CAP_CHANNEL_TYPE_CHANNEL_ECBM     // Classic + LE
} l2cap_channel_type_t;

```

在蓝牙协议栈中，L2CAP（Logical Link Control and Adaptation Protocol）支持多种通道类型，用于满足不同的通信需求。以下是这些通道类型的解释：

| 通道类型                            | 描述                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| `L2CAP_CHANNEL_TYPE_CLASSIC`        | 经典蓝牙的基本模式（Basic Mode）或增强重传模式（Enhanced Retransmission Mode, ERTM）。适用于传统蓝牙设备之间的数据传输，提供可靠或不可靠的通信。 |
| `L2CAP_CHANNEL_TYPE_CONNECTIONLESS` | 经典蓝牙的无连接模式。允许数据在不建立逻辑通道的情况下传输，适合需要广播或组播传输的应用。 |
| `L2CAP_CHANNEL_TYPE_CHANNEL_CBM`    | 用于LE（低功耗）设备。CBM可能代表LE中的“连接模式”，即数据在已建立连接的设备之间传输。 |
| `L2CAP_CHANNEL_TYPE_FIXED_LE`       | 低功耗设备的固定通道类型。包括LE设备中的ATT（Attribute Protocol）和SM（Security Manager Protocol），这些通道有固定的CID，用于特定的协议通信。 |
| `L2CAP_CHANNEL_TYPE_FIXED_CLASSIC`  | 经典蓝牙的固定通道类型。通常用于经典蓝牙中的安全管理（Security Manager）协议。这些通道的CID是固定的，专门用于特定的控制和管理任务。 |
| `L2CAP_CHANNEL_TYPE_CHANNEL_ECBM`   | 经典蓝牙和LE双模设备的增强通道类型。支持经典蓝牙和LE设备之间的通信，可能包括增强的特性和功能。 |

### 详细解释

1. **L2CAP_CHANNEL_TYPE_CLASSIC**:
   - **Basic Mode**：不提供错误恢复机制，适用于对丢包不敏感的应用。
   - **ERTM (Enhanced Retransmission Mode)**：提供可靠的数据传输，通过重传机制确保数据完整性。

2. **L2CAP_CHANNEL_TYPE_CONNECTIONLESS**:
   - 无需建立L2CAP通道的无连接数据传输方式，通常用于广播数据，如蓝牙设备发现（device discovery）。

3. **L2CAP_CHANNEL_TYPE_CHANNEL_CBM**:
   - 用于LE设备的连接模式，保证在建立连接的设备之间进行数据传输。通常应用于LE Audio、LE Secure Connections等场景。

4. **L2CAP_CHANNEL_TYPE_FIXED_LE**:
   - 包括ATT和SM协议在内的LE设备专用通道。这些通道的CID是固定的，例如ATT通常使用CID 0x0004。

5. **L2CAP_CHANNEL_TYPE_FIXED_CLASSIC**:
   - 经典蓝牙中的固定通道，通常用于特定管理任务如安全管理。

6. **L2CAP_CHANNEL_TYPE_CHANNEL_ECBM**:
   - 增强的通道类型，支持经典和LE双模设备。可能用于那些需要兼容两种设备的高级应用场景。

这些通道类型帮助L2CAP适应不同的应用需求和设备类型，从而支持多样化的蓝牙通信。

# 信道模式

逻辑信道有5种模式。

1、基本模式。这个是默认的模式。

2、流控模式。这个模式下，不会重传，但是丢失的数据可以被检测到。

3、重传模式。

4、streaming模式。这个模式下，数据包被编号，但是不会等待ACK。

5、BLE流控。







![](/images/L2CAP在协议栈里的位置.png)

由上面的图可以得到这些信息：

1、L2CAP在ACL之上。可以传控制信息。是异步的。

2、L2CAP是协议栈里的重要中枢。

btstack代码里：

```
#define COMPLETE_L2CAP_HEADER (HCI_ACL_HEADER_SIZE + L2CAP_HEADER_SIZE)
```



包头是这样：

```
len(2 bytes)| chn id(2 bytes) | payload |
```



既然len是2个字节，那么最大的L2CAP包长度就是64K。



L2CAP 基于 通道(channel) 的概念。 通道 (Channel) 是位于基带 (baseband) 连接之上的逻辑连接。每个通道以多对一的方式绑定一个单一协议 (single protocol)。**多个通道可以绑定同一个协议，但一个通道不可以绑定多个协议。** 



L2CAP编程非常重要，它和HCI基本就是Linux Bluetooth编程的基础了。几乎所有协议的连接，断连，读写都是用L2CAP连接来做的。



# L2CAP 和 ACL 的关系

第一个提示是 Vol.3 Part.A 中的第 7.2 节“分段和重组”，“逻辑链路控制和适应协议 （L2CAP）”。

本节的图 7.2（见下文）显示了从 L2CAP 层开始到无线数据包结束的数据路径图。

发送到 L2CAP 层的数据传输请求被分解成多个 HCI 数据包并发送到硬件（蓝牙芯片）。

固件（嵌入式软件）重新组装数据包，重新分割成多段帧，并将其作为无线数据包传输。

![Example of fragmentation process.png](/_posts/images/random_name2/Example of fragmentation process.pngwidth=674&height=553&name=Example of fragmentation process.png)

从这图中我们还可以看出，

HCI和无线数据包不是一一对应的，

单个HCI数据包可以拆分为多个无线数据包，

这些操作都是在Link Manager链路控制器层执行的。

该规范表明，该层可以通过仅通过说“适当地组装 1、3 和 5 插槽数据包类型”来选择数据包类型，但没有明确指定什么是“合适的”。

抛开模糊的选择逻辑不谈，我们可以说“芯片固件选择ACL帧类型。在这个阶段，上层似乎不想这样做。



https://www.silextechnology.com/unwired/basics-of-asynchronous-connection-less-acl-bluetooth-communication-protocol





# L2CAP一般是传输哪些数据，请举出实际的数据包的例子进行具体分析

L2CAP（Logical Link Control and Adaptation Protocol）是蓝牙协议栈中的一层，负责为更高层的协议和应用提供数据传输服务。L2CAP在蓝牙中提供了数据分段和重组、数据多路复用、以及质量服务的支持。以下是L2CAP的实际应用及数据包分析的例子：

### L2CAP数据传输的典型应用

1. **音频数据传输**：A2DP协议使用L2CAP来传输音频流数据。
2. **控制信令**：AVRCP协议使用L2CAP来传输远程控制信令数据，例如播放、暂停、音量控制等。
3. **文件传输**：如蓝牙文件传输协议（OBEX）使用L2CAP传输文件数据。

### 实际数据包分析

以A2DP音频数据传输为例：

**1. 数据包结构概览：**

- **L2CAP Header**:
  - **Length**: 表示L2CAP数据包的长度（不包括L2CAP Header本身）。
  - **Channel ID (CID)**: 标识此数据包属于哪个L2CAP通道。

- **Payload**:
  - 包含实际的数据，如音频数据、控制信令等。

**2. A2DP音频数据包示例：**

假设我们传输一个SBC编码的音频数据帧，L2CAP数据包的结构如下：

```
L2CAP Header
-------------
Length: 0x0030    // 包含数据的长度（48 bytes）
CID: 0x0040       // A2DP的CID（0x0040 表示此通道为AVDTP）
```

**Payload (实际数据)**
```
0x80 0x60 0x00 0x1f 0x9c 0x80 0x61 0x1f
0x3b 0x6e 0x80 0x62 0x07 0xd8 0xe0 0x80
0x63 0x6b 0x3e 0xe8 0x80 0x64 0x5a 0xf1
0x8f 0x80 0x65 0xa3 0xc1 0xa8 0x80 0x66
0x1f 0xbe 0x3a 0x80 0x67 0x51 0x92 0x88
0x80 0x68 0x09 0xa7 0x42 0x80 0x69 0x12
0xc4 0xe9 0x80 0x6a 0x07 0x3c 0x92 0x80
0x6b 0x58 0xf1 0xa8 0x80 0x6c 0x9b 0xe1
0xb9 0x80 0x6d 0x71 0xb6 0x54 0x80 0x6e
0x13 0xc1 0xef 0x80 0x6f 0x28 0x9f 0x61
```

- **Length**: 0x0030 表示数据部分长度为48字节。
- **CID**: 0x0040 表示这是A2DP音频数据。
- **Payload**: 实际传输的音频数据。上述示例中的数据为SBC编码的音频帧。

### 分析：

1. **L2CAP Header**：
   - **Length**字段表示后续有效数据的字节数，这对于接收方重组和处理数据非常重要。
   - **CID**标识数据的目的地协议或应用。例如0x0040用于A2DP的音频数据通道。

2. **Payload**：
   - 数据负载部分可以是多种类型的数据，例如音频流、控制指令或文件数据。在此示例中，负载部分为SBC编码的音频帧。

### 总结：

L2CAP是蓝牙协议中至关重要的一部分，它为高层协议提供了一致的数据传输服务。通过L2CAP传输的数据包不仅可以是音频数据，还可以是各种控制信令和应用数据。L2CAP数据包的具体结构和内容取决于其上层协议和应用需求。

# 蓝牙的psm是指什么

在蓝牙协议中，**PSM（Protocol/Service Multiplexer）**是一个重要的概念，用于区分不同的协议或服务。在L2CAP（Logical Link Control and Adaptation Protocol）层，PSM值用于标识不同的上层协议或服务。

### PSM的作用

PSM值是L2CAP协议的一个字段，它允许多个协议或服务在同一个物理连接上共存。每个PSM值都代表一个特定的协议或服务，当设备建立L2CAP通道时，PSM值用于指示所使用的具体协议或服务类型。

### 常见的PSM值

以下是一些常见的PSM值及其对应的协议或服务：

| **PSM值** | **协议/服务**                                                |
| --------- | ------------------------------------------------------------ |
| 0x0001    | SDP（Service Discovery Protocol） - 服务发现协议             |
| 0x0003    | RFCOMM - 仿真串口通信协议                                    |
| 0x0005    | TCS-BIN（Telephony Control Protocol Specification） - 电话控制协议 |
| 0x0007    | BNEP（Bluetooth Network Encapsulation Protocol） - 蓝牙网络封装协议 |
| 0x000F    | HID Control - 人机接口设备控制通道                           |
| 0x0011    | HID Interrupt - 人机接口设备中断通道                         |

### PSM值的范围

- **预定义范围**：0x0001到0xFFFF之间的PSM值用于标准化协议和服务。PSM值必须是奇数，且高位字节的最低有效位（least significant bit）必须为1。
- **动态分配**：0x0000是无效的PSM值，0x0002是保留值。其他奇数PSM值可以由设备动态分配给特定的应用程序或协议。

### 使用场景

- 当蓝牙设备要使用某种服务或协议时，设备会请求对应的PSM值。例如，当两个设备之间需要建立RFCOMM连接时，设备会使用PSM值0x0003来标识这个协议。
- PSM值在建立L2CAP通道时被使用，以确定数据流的目的地。例如，如果主机想要与蓝牙设备上的SDP服务器通信，它会向控制器发送一个包含PSM值0x0001的L2CAP连接请求。

### 重要性

PSM在蓝牙协议栈中起到多路复用的作用，允许多个服务和协议在同一物理连接上并发运行，确保数据能够准确地路由到合适的上层协议或服务。

# 参考资料

1、蓝牙核心-L2CAP

https://blog.csdn.net/u010657219/article/details/42105193

2、蓝牙L2CAP剖析（一）

https://blog.csdn.net/XiaoXiaoPengBo/article/details/51364483

3、Bluetooth L2CAP介绍

https://www.cnblogs.com/hzl6255/p/3801732.html

4、

http://blog.sina.com.cn/s/blog_69b5d2a50101ehpv.html

5、这个文档非常好。

https://www.baidu.com/link?url=SyC_Ni5xYoT_IjLarhImjibVcd5T5upVdgL0OTS_LkeMjAba9XaN8GhkY_CamMyeldEsHOZfSMq_BKuYlXjLuKgbgLL90Nm4iDrtQs_h3YzgCtdfNgRvngum29SngxTH&wd=&eqid=94a431e30026855f000000065ebdfd73

6、蓝牙协议系列之（四） L2CAP

https://blog.csdn.net/zwc1725/article/details/80704678

7、实战Linux Bluetooth编程（四） L2CAP层编程

https://blog.csdn.net/rain0993/article/details/8533246