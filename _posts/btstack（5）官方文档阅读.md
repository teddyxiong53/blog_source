---
title: btstack（5）官方文档阅读
date: 2019-03-07 16:37:35
tags:
	- btstack
typora-root-url: ../
---





# 架构

如同其他的通信协议栈一样，btstack是一组状态机之间的交互。

每个子协议都有1个或者多个状态机。

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

btstack是支持经典蓝牙和ble的。

ble的改进是：

1、功耗低。

2、连接更快。

3、同时连接的设备更多。

![](/images/btstack的协议栈图.png)

## hci

hci提供对蓝牙芯片的命令接口。

在btstack的实现里，hci的实现也跟踪了所有的活动连接。还处理了L2CAP包的分片和重组。

注意，应用层一般不会调用hci层的接口。

btstack提供了GAP层的接口。这里面封装了HCI接口。

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

## RFCOMM

rfcomm提供在L2CAP上的串口模拟。

是HFP / HSP / OBEX的基础。

也是spp的基础。

因为模拟的是串口，所以没有包边界。

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

用来声明自己可以提供的服务，和获知对方可以提供的服务。

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



## GAP

GAP定义了设备如何发现对方，如何建立安全连接。

让自己可被发现

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



# 已实现的GATT服务

电池服务

心率服务





那些send函数，都没有真正发送，是靠触发select来做的。



参考资料

1、官方资料

http://bluekitchen-gmbh.com/btstack/architecture/