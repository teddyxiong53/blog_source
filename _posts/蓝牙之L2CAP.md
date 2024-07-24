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



谈起应用程序，就不得不说BLE的初衷----物联网。

物联网中传输的数据和传统的互联网有什么区别呢？抛开其它不谈，物联网中最重要、最广泛的一类应用是：信息的采集。

这些信息往往都很简单，如温度、湿度、速度、位置信息、电量、等等。

采集的过程也很简单，节点设备**定时的向中心设备汇报**信息数据，或者，中心设备在需要的时候**主动查询**。

基于信息采集的需求，BLE抽象出一个协议：Attribute protocol，该协议将这些“信息”以“Attribute（属性）”的形式抽象出来，并提供一些方法，供远端设备（remote device）读取、修改这些属性的值（Attribute value）。

Attribute Protocol的主要思路包括：
**1）基于L2CAP，使用固定的Channel ID。就是0x0004。**

2）采用client-server的形式。提供信息（以后都称作Attribute）的一方称作ATT server（一般是那些传感器节点），访问信息的一方称作ATT client。

3）一个Attribute由Attribute Type、Attribute Handle和Attribute Value组成。



ATT之所以称作“protocol”，**是因为它还比较抽象，仅仅定义了一套机制，**允许client和server通过Attribute的形式共享信息。

**而具体共享哪些信息，ATT并不关心，这是GATT（Generic Attribute Profile）的主场。**

GATT相对ATT只多了一个‘G‘，但含义却大不同，因为GATT是一个profile（更准确的说是profile framework）。

在蓝牙协议中，profile一直是一个比较抽象的概念，**我们可以将其理解为“应用场景、功能、使用方式”都被规定好的Application。**

传统的BR/EDR如此，BLE更甚。上面我们讲过，**BLE很大一部分的应用场景是信息（Attribute）的共享**，因此，BLE协议栈基于Attribute Protocol，定义了一个称作GATT（Generic Attribute）的profile framework（它本身也是一个profile），用于提供通用的、信息的存储和共享等功能。

GATT profile的层次结构依次是：Profile—>Service—>characteristic。

“Profile”是基于GATT所派生出的真正的Profile，位于GATT Profile hierarchy的最顶层，由一个或者多个和某一应用场景有关的Service组成。

一个Service包含一个或者多个Characteristic（特征），也可以通过Include的方式，包含其它Service。

Characteristic则是GATT profile中最基本的数据单位，由一个Properties、一个Value、一个或者多个Descriptor组成。

Characteristic Properties定义了characteristic的Value如何被使用，以及characteristic的Descriptor如何被访问。
Characteristic Value是特征的实际值，例如一个距离特征，其Characteristic Value就是距离长度。
Characteristic Descriptor则保存了一些和Characteristic Value相关的信息（例如value记录距离长度，那么Descriptor可以是长度单位m/km）。

**以上除“Profile”外的每一个定义，Service、Characteristic、Characteristic Properties、Characteristic Value、Characteristic Descriptor等等，都是作为一个Attribute存在的，包括之前所描述的Attribute的所有特征：Attribute** 





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