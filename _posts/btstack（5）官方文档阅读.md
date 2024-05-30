---
title: btstack（5）官方文档阅读
date: 2019-03-07 16:37:35
tags:
	- btstack
typora-root-url: ../
---





# 架构

**如同其他的通信协议栈一样，btstack是一组状态机之间的交互。**

**每个子协议都有1个或者多个状态机。**

主要的设计原则：

```
1、单线程设计。
	使用一个single run loop。处理数据和timer。
	
2、所有地方都不阻塞。通过事件的机制分发处理。
	蓝牙的逻辑是event驱动的。
	
3、不排队收发的包。这样就不会有限制大小。
	这个需要蓝牙芯片在需要的时候，把速度压慢一点。
	
4、可以静态分配内存。
```



BTstack 不使用或不需要多线程。

它使用单个运行循环来处理数据源和计时器。

数据源代表通信接口，

例如 UART 或 USB 驱动程序。 

BTstack 使用定时器来实现各种与蓝牙相关的超时。

例如，在 20 秒后断开没有活动 L2CAP 通道的蓝牙基带通道。

它们还可以用于处理周期性事件。

在一个运行循环周期中，所有注册数据源的回调函数都会被调用。

然后执行准备好的定时器的回调函数。



==蓝牙逻辑是事件驱动的。==

因此，所有 BTstack 函数都是非阻塞的，即所有不能立即返回的函数都实现异步模式。

如果函数的参数有效，则必要的命令将发送到蓝牙芯片组，并且函数会返回成功值。

实际结果稍后通过注册的数据包处理程序作为异步事件传递。





# 配置btstack的方法

btstack实现了一组蓝牙协议栈和profile。

为了连接到其他蓝牙设备，或者提供一些服务。btstack需要正确的配置。

配置分为2部分：

```
1、编译时配置。
	修改btstack_config.h 里的内容。
2、运行时配置。
```



# 协议

BTstack 是一个模块化双模蓝牙堆栈，

支持蓝牙基本速率/增强数据速率 (BR/EDR) 以及蓝牙低功耗 (LE)。 

BR/EDR 技术也称为经典蓝牙，

可在专为高数据速率设计的设备之间提供强大的无线连接。

相比之下，LE 技术的吞吐量较低，

但能耗也较低、连接设置速度更快，并且能够并行连接更多设备。



无论是 Classic 还是 LE，蓝牙设备都会实现一个或多个蓝牙配置文件。

==蓝牙配置文件指定如何使用一个或多个蓝牙协议来实现其目标。==

例如，每个蓝牙设备都必须实现通用访问配置文件 (GAP)，它定义设备如何找到彼此以及如何建立连接。

该配置文件主要利用主机控制器接口（HCI）协议，这是堆栈层次结构中的最低协议，它实现了蓝牙芯片组的命令接口。

(GAP直接对接到HCI层上，是一个最基础的服务)

除了 GAP 之外，一个流行的经典蓝牙示例是可以通过串行端口配置文件 (SPP) 连接的外围设备。 

SPP 基本上指定兼容设备应提供包含 RFCOMM 通道号的服务发现协议 (SDP) 记录，该记录将用于实际通信。

==同样，对于每个 LE 设备，除了 GAP 之外，还必须实现通用属性配置文件 (GATT) 配置文件。== 

GATT 构建在属性协议 (ATT) 之上，定义一台设备如何与远程设备上的 GATT 服务交互。





![](/images/btstack的协议栈图.png)

## hci

hci提供对蓝牙芯片的命令接口。

在btstack的实现里，hci的实现也跟踪了所有的活动连接。还处理了L2CAP包的分片和重组。

**注意，应用层一般不会调用hci层的接口。**

**btstack提供了GAP层的接口。这里面封装了HCI接口。**

例如，设置名字，你调用gap_set_local_name函数就好了。

需要使用hci接口的场景是：在启动过程中，用来做那些GAP接口里还没有提供的功能。

那么如何定义一个hci命令呢？

```
每个HCI命令分别2个字节的操作码。这个就是命令号。
命令号被分为2个部分：
命令组号。OpCode Group Field。缩写OGF。
命令号。OpCode Command Field。缩写OCF。

这样进行组合。
// Calculate combined ogf/ocf value.
#define OPCODE(ogf, ocf) (ocf | ogf << 10)
```

OGF有这些：

```
// OGFs
#define OGF_LINK_CONTROL          0x01
#define OGF_LINK_POLICY           0x02
#define OGF_CONTROLLER_BASEBAND   0x03
#define OGF_INFORMATIONAL_PARAMETERS 0x04
#define OGF_STATUS_PARAMETERS     0x05
#define OGF_TESTING               0x06
#define OGF_LE_CONTROLLER 0x08
#define OGF_VENDOR  0x3f
```

## L2CAP

L2CAP支持更上层的协议多路复用和分包。

它是RFCOMM和BNEP协议的基础。

L2CAP是基于通道的概念的。

一个通道是一个逻辑连接，建立在基带连接之上。

一个通道绑定一个协议。

多个通道可以绑定到同一个协议。

要跟remote设备的L2CAP服务进行通信，需要做这些事情：

```
l2cap_init 
l2cap_create_channel 创建一个outgoing的通道
	会创建一个新的基带连接，如果还不存在的话。
l2cap_packet_handler 注册这个函数。
```

如果本设备要对外提供L2CAP服务，应该这么做：

```
l2cap_init
l2cap_register_service
l2cap_accept_connection 
或者
l2cap_deny_connection 

l2cap_send
```

发送L2CAP数据

```
发送L2CAP数据可能会失败，如果发得太快的话。
可以用l2cap_request_can_send_now_event这个判断一下。
```

LE数据通道

```
就是上面协议栈图里的L2CAP LE。
l2cap_le_register_service 
l2cap_le_accept_connection 
```

## LE 数据通道

LE 数据通道的完整名称

实际上是具有基于 LE 信用的流量控制模式的 LE 连接导向通道。

在此模式下，数据作为服务数据单元 (SDU) 发送，该单元可能大于单个 HCI LE ACL 数据包。

LE 数据通道类似于经典 L2CAP 通道，

但也提供类似于 RFCOMM 通道的基于信用的流量控制。

除非使用蓝牙核心 4.2 规范的 LE 数据包扩展，

否则 LE ACL 数据包的最大数据包大小为 27 字节。

==为了发送更大的数据包，每个数据包将被拆分为多个 ACL LE 数据包并在接收端重新组合。==



## RFCOMM

rfcomm提供在L2CAP上的串口模拟。

**是HFP / HSP / OBEX的基础。**

也是spp的基础。

**因为模拟的是串口，所以没有包边界。**

在大多数的os上，rfcomm/spp被看成一个pipe。写入一段数据，长度没有上面规定。

我们需要在前面加上长度，然后在接收端根据这个长度值进行重组。



访问remote设备的rfcomm服务

```
rfcomm_init 
rfcomm_create_channel_with_initial_credits 
rfcomm_packet_handler
```

提供一个rfcomm服务

```
rfcomm_register_service
rfcomm_accept_connection 
rfcomm_deny_connection 
```



降低rfcomm接收数据的速度

```

```

## SDP

服务发现协议。

**用来声明自己可以提供的服务，和获知对方可以提供的服务。**

创建和宣布SDP记录

```
btstack包含一个完整的sdp server。允许注册sdp records。
一个sdp record是这样的格式：
{ID, Value}
ID是16bit的。
Value可以是字符串、整数，也可以是另外一个记录。

要给spp创建一个sdp record。
你可以调用spp_create_sdp_record 
```



查询remote的sdp 服务

```
btstack提供了一个sdp client，用来查询sdp service。
sdp_client_query
```



# profiles

## A2DP - Advanced Audio Distribution



A2DP 配置文件定义如何通过蓝牙连接将音频从一个设备（例如移动电话）传输到另一设备（例如耳机）。

充当音频流源的设备实现 A2DP 源角色。

同样，接收音频流的设备实现 A2DP Sink 角色。

因此，A2DP 服务允许音频流的单向传输，从单声道单声道到双声道立体声。

我们的实施包括对SBC 编解码器的强制支持。

还支持可选代码（FDK AAC、LDAC、APTX）的信令，您需要提供自己的编解码器库。

## AVRCP - Audio/Video Remote Control Profile

AVRCP 配置文件定义了如何控制远程设备（例如智能手机上的音乐应用程序）上的音频播放，

以及如何从远程接收状态更改，

例如音量、当前播放媒体的信息、电池等。

设备（例如扬声器）。通常，每个设备实现两个角色：

- 控制器角色。允许查询当前播放媒体的信息，例如标题、艺术家和专辑，以及控制播放，即播放、停止、重复等。 
- 目标角色响应命令，例如播放控制和查询，例如播放状态、媒体信息，来自控制器当前播放的媒体。



## GAP - Generic Access Profile: Classic

GAP定义了设备如何发现对方，如何建立安全连接。

让自己可被发现

远程未连接的蓝牙设备必须设置为“可发现”，

以便执行查询扫描的设备能够看到。

要变得可发现，应用程序可以使用输入参数 1 调用gap_discoverable_control。

如果您想为设备提供有用的名称，应用程序可以通过调用gap_set_local_name 设置其本地名称。

为了节省能源，一旦建立连接，您可以再次将设备设置为不可发现。



要扫描远程设备，请使用 hci_inquiry 命令。

每个响应至少包含蓝牙地址、设备类别、寻呼扫描重复模式以及找到的设备的时钟偏移。

后面的事件添加有关接收信号强度的信息或提供扩展查询结果 (EIR)。下面的清单中显示了代码片段。

默认情况下，既不报告 RSSI 值，也不报告 EIR。如果蓝牙设备实现蓝牙规范 2.1 或更高版本，则 hci_write_inquiry_mode 命令可启用此高级功能的报告（0 表示标准结果，1 表示 RSSI，2 表示 RSSI 和 EIR）。



```
gap_discoverable_control 
一般为了降低功耗，在建立连接后，一般又把自己设为不可见了。gap_discoverable_control(0);
```

设备配对

```
默认情况下，蓝牙通信是没有授权的。
任何设备都可以相互通信。
为了安全，你可以打开授权要求。

在蓝牙2.0之前，需要一个pin码。
在建立连接的2个设备都需要进行输入。

这个对于嵌入式设备，其实是很不友好。

蓝牙2.1开始引入了Secure Simple Pairing（SSP）。

无论是PIN还是SSP方式，在成功后，都会生成一个link key。
以后就可以直接连接了。

```

## SPP - Serial Port Profile

SPP 配置文件定义了如何设置虚拟串行端口并连接两个支持蓝牙的设备。

请记住，如果您尝试将数据作为数据包发送并阅读有关 RFCOMM 数据包边界的信息，则串行端口不会保留数据包边界。

### 访问远程设备上的 SPP 服务器


要访问远程SPP服务器，

首先需要查询远程设备的SPP服务。

查询远程 SDP 服务部分展示了如何查询所有 RFCOMM 通道。

对于 SPP，您可以执行相同的操作，但使用 SPP UUID 0x1101 进行查询。

确定正确的 RFCOMM 通道后，您可以创建 RFCOMM 连接，如下所示。

### 提供 SPP 服务器

要提供 SPP 服务器，

您需要提供具有特定 RFCOMM 通道号的 RFCOMM 服务，

如 RFCOMM 服务部分中所述。

然后，您需要为其创建一条SDP记录，

并通过调用sdp_register_service将其发布到SDP服务器。 

BTstack 提供了 spp_create_sdp_record 函数，

该函数需要大约 200 字节的空缓冲区、服务通道号和服务名称。

查看 SPP 计数器示例。

## PAN - Personal Area Networking Profile

## HSP - Headset Profile

HSP 配置文件定义了蓝牙耳机应如何与其他蓝牙设备进行通信。它依靠 SCO 以 64 kbit/s CVSD 编码的音频，以及来自 GSM 07.07 的 AT 命令子集来实现最小控制，包括响铃、接听电话、挂断电话和调节音量的功能。

# 已实现的GATT服务

电池服务

心率服务





那些send函数，都没有真正发送，是靠触发select来做的。



参考资料

1、官方资料

http://bluekitchen-gmbh.com/btstack/architecture/