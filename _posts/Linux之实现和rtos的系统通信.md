---
title: Linux之实现和rtos的系统通信
date: 2022-05-11 11:20:01
tags:

	- Linux

---

--

stm32mp157的跨核通信在linux侧是基于 RPMsg 服务面向 Linux 用户空
间提供“/dev/ttyRPMSG”串口节点收发数据，在M4侧则是基于 OpenAMP 库调用虚拟串口函数“virtual_hal_uart()”收发数据。应用角度来看类似于串口透传，硬件角度来看，信号通知(Mailbox)服务基于内部 IPCC(Inter-Processor communicationcontroller)，数据传输基于共享内存。



通常在AMP（非对称多处理）配置中，

会采用在不同的处理核上运行不同的软件环境并执行各自的代码程序，

各核心之间通力合作实现处理器性能的提升。

在AMP系统中，

所谓的主处理器

通常是指最先启动

且主要负责管理其他CPU以及这些CPU上软件环境的CPU处理器。

而远程处理器简单的讲就是指被主核所支配的CPU。

主软件环境通常需要进行远程核心的管理以及任务调度，

在需要进行计算任务分配时，将选择性地驱动远程内核上的远程软件环境，并交代任务信息。



OpenAMP软件[框架](https://so.csdn.net/so/search?q=框架&spm=1001.2101.3001.7020)为开发AMP系统提供了必要的API函数。

OpenAMP 是Mentor Graphics 与赛灵思公司

为了使在AMP系统的设计中开发出的RTOS和裸机程序能够与开源Linux社区提供的接口进行互通讯，

而共同通过的一个标准化的嵌入式多核框架。

的全称是 ,即开源的非对称多处理框架。

OpenAMP框架提供了非对称多处理系统软件开发所需的软件组件。

OpenAMP框架是一种软件框架，这种软件框架能够为非对称多处理(AMP)系统开发人员提供三大重要组件：

https://github.com/OpenAMP/open-amp





参考资料

1、五、建立M4 rtos和A7 linux之间的通信

https://blog.csdn.net/qq_24622489/article/details/121195731

2、核间通信openamp 在linux内核空间

https://blog.csdn.net/wangyongzixue/article/details/121236853

3、OpenAMP简介

https://blog.csdn.net/qq_35510898/article/details/108796797

4、

https://blog.csdn.net/wuhenyouyuyouyu/article/details/104668858