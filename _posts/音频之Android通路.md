---
title: 音频之Android通路
date: 2019-06-22 09:27:37
tags:
	- 音频
---

1

Android支持多种设备的的输出。

一台正常的机子，

本身就自带话筒，扬声器，麦克风等多个声音输入输出设备，

再加上五花八门的外置设备（通过耳机，蓝牙，wifi等方式连接），

使声音的输出更具多样性。

Android支持如此多的设备连接，

那么android内部是怎样对设备的输出输出进行控制的呢？

这一次我们主要来看看音频通路的切换。



要想知道Andorid是怎样对设备的输出输出进行控制的，

我们首先来了解一些音频相关的基本知识：

 stream_type、content_type、devices、routing_strategy。

stream_type:音频流的类型。

在当前系统中，Android(6.0)一共定义了11种stream_type以供开发者使用。

Android上层开发要想要发出声音，都必须先确定当前当前的音频类型。

content_type:具体输出类型。

虽然当前一共有11种stream_type,但一旦进入到Attribute，Android就只将其整理成几种类型。

这才是实际的类型。

device:音频输入输出设备。

Android定义了多种设备输入输出设备（具体物理设备可能还是那几个，但是输出场景不尽相同）。

routing_strategy:音频路由策略。

默认情况下，Android是根据路由策略去选择设备负责输出输入音频的。



在了解完Audio一些基本的定义设定之后，我们来看一下Android的Audio整体架构。

Audio内部系统从上到下包含各方面的东西。

对于声音输出的设备的选择与切换，我们主要需要关注2个地方。

第一处，是外接设备如耳机，蓝牙设备等连接的通知。

第二处就是Audio系统中核心的AudioFinger与AudioPolicyService的处理内容。

AudioFinger是Audio系统的工作引擎，

管理着系统中输入输出音频流，并承担音频数据混音，

以及读写Audio硬件等工作以实现数据的输入输出功能。

AudioPolicyService是Audio系统策略控制中心，

具体负责掌管系统中声音设备的选择和切换，音量控制等功能。



基本的声音输出调用

发出声音是Android机器的一个最基本的功能。

但是，Android是怎么发出声音的呢？

就算不连接外设，Android最基本还有听筒和扬声器2个设备。

那么，Android内部，是怎么控制他们2个发出声音的呢？

下面我们来具体看 一下Android一般情况下发出声音时选择设备的过程。

我们要想分析Android中的声音输出，

当然是先通过播放音频去一步一步了解Android是怎么输出声音的。

下面我们以一个最简单的AudioTrack播放音频为例，来看下Android的发生过程。



参考资料

1、简单聊一下Android音频通路的切换

https://blog.csdn.net/u012440406/article/details/54883220

