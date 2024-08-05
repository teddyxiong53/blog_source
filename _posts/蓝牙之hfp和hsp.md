---
title: 蓝牙之hfp和hsp
date: 2022-04-21 19:41:11
tags:
	- 蓝牙

---

--

# hfp和hsp关系

一、前言
有时，我们能看到有的蓝牙产品标明支持HFP/HSP，而有的产品却只标注了支持HFP，那么HFP or HSP是什么呢？又有什么样的关系呢？

二、HSP协议
HSP（Headset Profile），耳机模式
仅实现了最基本的通话操作：接听电话、挂断电话、调节音量、声音在手机/蓝牙耳机之间切换。
1
2
三、HFP协议
HFP(Hands-free Profile)，免提模式，
是在HSP上的扩展，除了上述功能以外，还包括控制三方通话、来电拒接、耳机端来电显示等高级功能，
不过实现的方式，和用于控制的AT CMD完全不一样。

目前HFP的使用场景有车载蓝牙，耳机和PDA，定义了AG和HFP两种角色。
AG（Audio Gate）音频网关—音频设备输入输出网关；
HF（Hands Free）免提—该设备作为音频网关的远程音频输入/输出机制，并可提供若干遥控功能。

在车载蓝牙中，手机侧是AG，车载蓝牙侧是HF，在android源代码中，将AG侧称为HFP/AG，将HF侧称为HFPClient/HF。

四、总结
HFP(Hands-free Profile)和HSP（Headset Profile）都是为了实现蓝牙通话而制定的，所实现的功能都和蓝牙通话相关。基本所有的蓝牙耳机、车载蓝牙都会支持这两个协议。

在Android设计上并没有将上述两个协议分开显示，而是均表述为“手机音频”，在使用的时候优先连接HFP，只有在对方仅支持HSP或HFP连接失败的时候才会尝试连接HSP。

# hfp跟rfcomm什么关系

**HFP（Hands-Free Profile）** 和 **RFCOMM（Radio Frequency Communication）** 是蓝牙协议栈中的两个不同层次的协议，它们在蓝牙通信中扮演不同的角色，但它们之间存在一定的关系。

### HFP（Hands-Free Profile）

- **定义**：HFP是一种蓝牙配置文件（Profile），用于在车载系统和手机之间实现免提通信（如语音通话）。它定义了如何通过蓝牙进行电话控制、语音通话等操作。
- **功能**：HFP允许手机通过车载系统进行语音拨号、接听电话、控制音量等操作。它定义了一系列的命令和事件，用于管理电话功能。

### RFCOMM（Radio Frequency Communication）

- **定义**：RFCOMM是蓝牙协议栈中的一个层次，负责提供串行数据通信。它是基于蓝牙的L2CAP（Logical Link Control and Adaptation Protocol）层的一个协议，为应用程序提供类似于串行端口的服务。
- **功能**：RFCOMM允许在蓝牙设备之间建立虚拟串行端口，通过该端口传输数据。它支持多个应用之间的串行数据传输，包括支持HFP、OBEX（Object Exchange）、和其他需要串行通信的服务。

### HFP与RFCOMM的关系

1. **依赖关系**：
   - HFP依赖RFCOMM来进行数据传输。==HFP使用RFCOMM来建立一个虚拟的串行端口，通过这个端口发送和接收电话控制和语音数据。==
   - 具体来说，HFP协议中的数据（如控制命令、语音数据等）通过RFCOMM通道进行传输。这意味着HFP的控制信息和数据流实际上是在RFCOMM建立的通道上交换的。

2. **工作流程**：
   - **连接建立**：当HFP设备（如车载系统）和手机之间建立连接时，HFP协议会通过RFCOMM建立一个虚拟串行端口。
   - **数据传输**：一旦RFCOMM通道建立，HFP可以通过这个通道发送电话控制命令、接收通话状态、以及传输语音数据等。
   - **命令和事件**：HFP协议定义了各种命令和事件（如拨号、接听电话），这些命令和事件通过RFCOMM通道传递给对端设备。

### 总结

- **HFP** 是蓝牙配置文件，定义了免提通信的标准和操作。
- **RFCOMM** 是蓝牙协议层，提供了串行数据通信服务，用于在蓝牙设备之间建立虚拟串行端口。
- **HFP与RFCOMM的关系**：HFP通过RFCOMM来传输数据，RFCOMM提供了HFP所需的数据传输通道。

简单来说，HFP使用RFCOMM来实现其功能，RFCOMM为HFP提供了必要的通信基础设施，使HFP能够在蓝牙设备之间进行免提电话控制和语音通话。



io_thread_sco

hci_open_sco



# 参考资料

1、

https://blog.csdn.net/zhanghuaishu0/article/details/107198830