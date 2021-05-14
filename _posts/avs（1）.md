---
title: avs（1）
date: 2018-05-09 21:03:10
tags:
	- avs

---



avs是Alexa Voice Service。



# 核心依赖

1、c++11版本以上。

2、gcc 4.8.5或者clang 3.3

3、cmake 3.1 。

其他。

# 媒体播放器依赖

1、gstreamer1.10.4以上版本。



# sample app的依赖

1、PortAudio

2、gstreamer。



# 代码分析

Alexa语音服务允许开发者通过麦克风和扬声器为连接的产品提供语音功能.

一旦集成,你的产品将有权访问Alexa内置功能(如音乐播放、定时器和闹钟、快递追踪、电影列表、日历管理等)

以及使用Alexa技能工具包开发的第三方技能。

AVSDevice SDK 提供基于C ++（11或更高版本）的库，

利用 AVS API 为 Alexa 启用的产品创建设备软件。

它是模块化和抽象的，提供用于处理离散功能（如语音捕获，音频处理和通信）的组件，

**每个组件都会显示可以使用和定制的API，用于集成。**

它还包括一个示例应用程序，演示与AVS的互动

![img](../images/random_name/20180521155249650)

上图说明了构成用于 C++ 的 AVS Device SDK 的组件之间的数据流

Audio Signal Processor：算法处理模块。所应用的算法被设计用于产生干净的音频数据，包括回声消除，波束形成，语音活动检测等。如果存在多麦克风阵列，则 ASP 构建并输出阵列的单个音频流。

SharedData Stream：共享数据流主要有两个作用，1.在发送到 AVS 之前，在ASP、唤醒语引擎ACL之间传递音频数据。2，通过 Alexa 通信库将由 AVS 发送的数据内容，传递给特定能力的代理。

Audio Input Process：用于处理通过 ACL 发送到 AVS 的音频输入。

Alexa Communications Library：提供消息发送和接收功能并建立和维护与AVS的长期持续连接。

Alexa Directive Sequencer Library：AVS指令集，接收从AVS Server接收到的指令，并送给指定的能力集代理处理。

 Mediaplayer：语音播放。




# 参考资料

1、Linux平台:Alexa语音服务快速入门指南

https://blog.csdn.net/z2066411585/article/details/78573368

2、wiki

https://github.com/alexa/avs-device-sdk/wiki

3、

https://blog.csdn.net/teksky163/article/details/80393304