---
title: 蓝牙之L2CAP
date: 2018-12-11 20:53:44
tags:
	- 蓝牙
typora-root-url: ../
---



L2CAP是Logic Link Control Adapter Protocol。

逻辑链路控制和适配协议。

重点是逻辑链路。逻辑二字。它的作用是为2个通信的蓝牙设备提供端到端的通道。

主要的作用是：

1、协议信道复用。

2、分段与重组。

3、信道流控。

4、error control。



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
1）基于L2CAP，使用固定的Channel ID。就是0x0004。
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

0x0002：这个是作为无连接的信道使用。无连接是指没有建立ACL通路。

0x0040到0xFFFF：这些信道是动态分配的。

如果是BLE设备，那么0x0005信道是作为BLE的信令通道。而0x0004和0x0006页会被强制分配给BLE，作为ATT和SecurityManager信道。

这些在btstack的源代码里，都可以看到的。

```
// L2CAP Fixed Channel IDs    
#define L2CAP_CID_SIGNALING                 0x0001
#define L2CAP_CID_CONNECTIONLESS_CHANNEL    0x0002
#define L2CAP_CID_ATTRIBUTE_PROTOCOL        0x0004
#define L2CAP_CID_SIGNALING_LE              0x0005
#define L2CAP_CID_SECURITY_MANAGER_PROTOCOL 0x0006
```





信道模式

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



包头是这样：

```
len(2 bytes)| chn id(2 bytes) | payload |
```











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