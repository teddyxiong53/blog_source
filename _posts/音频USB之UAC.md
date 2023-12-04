---
title: 音频USB之UAC
date: 2023-02-09 13:34:17
tags:
	- 音频

---

--

uac是一个跟uvc类似的东西。

是通过usb来传输音频数据。

对应的驱动代码在这里：

kernel\aml-5.4\drivers\usb\gadget\function\f_uac2.c



# uac简介

USB Audio Class（UAC）是一种USB音频设备与计算机之间通信的标准协议。

它定义了USB音频设备应如何与计算机进行数据交换，以确保音频设备的兼容性和互操作性。

以下是一些关于USB音频UAC的重要信息：

1. **标准化接口：** UAC标准定义了音频设备与主机计算机之间的通信接口，这使得不同制造商的音频设备能够在不同操作系统上==无需额外的驱动程序==即可正常工作。这使得用户能够将USB麦克风、耳机、音频接口等设备插入计算机并立即使用，而不需要繁琐的安装过程。

2. **音频格式：** UAC支持各种音频格式，包括PCM（脉冲编码调制）、MIDI（音乐仪器数字接口）和其他音频编解码器。这意味着USB音频设备可以传输不同类型的音频数据。

3. **功能描述：** ==UAC定义了音频设备的功能描述，这些描述包括输入通道、输出通道、音频格式、采样率等信息。==主机计算机可以通过这些描述了解设备的功能和能力，以确保正确配置音频流。

4. **Plug and Play：** 通过UAC，USB音频设备变得非常容易使用，用户只需插入设备并等待操作系统自动识别设备并配置音频通道。这种即插即用的特性大大提高了设备的可用性和用户友好性。

5. **低延迟音频传输：** UAC也支持低延迟音频传输，这对于需要实时音频处理的应用程序非常重要，如音频录制、音频处理和音频通信。

总之，USB Audio Class是一个使USB音频设备更易于使用和互操作的标准，它为音频设备的制造商和用户提供了便利，同时也为开发者提供了一致的接口，以在不同平台上实现音频设备的兼容性。

# uac发展历史

USB Audio Class（UAC）的发展历史可以追溯到USB音频设备的出现和USB规范的不断演进。以下是一些关于UAC的发展历史里程碑：

1. **USB 1.0和USB 1.1：** 在早期的USB规范中，并没有专门定义用于音频设备的通信协议。因此，早期的USB音频设备通常需要特定的驱动程序来与计算机通信，这限制了它们的兼容性和易用性。

2. **USB 2.0：** 随着USB 2.0规范的发布，USB音频设备的兼容性得到改善，但仍然需要特定的驱动程序来支持不同设备。然而，音频设备的制造商开始寻求更一致的解决方案，以简化设备的使用。

3. **USB Audio Class 1.0：** 在2006年，USB Implementers Forum（USB-IF）发布了USB Audio Class 1.0规范，该规范定义了一种标准的音频设备通信协议，为音频设备制造商提供了一种更简单的方式来实现其设备的兼容性。==这标志着UAC的正式引入。==

4. **USB 3.0和USB 3.1：** 随着USB 3.0和USB 3.1规范的推出，USB音频设备获得了更高的数据传输速度，这对于高质量音频流的传输非常有益。

5. **USB Audio Class 2.0：** 在2013年，USB-IF发布了USB Audio Class 2.0规范，进一步扩展了UAC的功能，==支持更高的音频分辨率和多通道音频。==这一版本的规范提供了更多的灵活性和性能。

6. **USB Type-C和USB 3.2：** 随着USB Type-C接口和USB 3.2规范的推出，USB音频设备可以更方便地连接到计算机，并获得更高的数据传输速度。

7. **不断的演进：** UAC仍在不断演进，以适应新的音频技术和需求。USB-IF持续更新规范，以确保USB音频设备能够满足现代音频应用的要求，例如高分辨率音频、虚拟现实、实时音频处理等。

总的来说，UAC的发展历史表明了USB音频设备在易用性、兼容性和性能方面取得的显著进展，使其成为许多不同类型的音频应用的重要部分。

# 把树莓派做为一个uac设备

将树莓派配置为USB Audio Class（UAC）设备，以使其充当USB音频设备，需要一些额外的设置和编程。这通常涉及使用树莓派的USB OTG（On-The-Go）功能，并通过编程来模拟UAC设备的行为。以下是大致的步骤，但这需要一些深入的Linux系统和USB编程知识：

1. **确认硬件支持：** 首先，请确保您的树莓派型号支持USB OTG功能，因为不是所有型号都支持。一些型号如Raspberry Pi Zero和Raspberry Pi 4支持USB OTG。您还需要一个USB OTG适配器（Micro USB到USB A）来连接树莓派到目标计算机。

2. **配置USB OTG模式：** 树莓派需要配置为USB OTG模式，这通常涉及编辑树莓派的config.txt文件，以启用USB OTG。

3. **编程模拟UAC设备：** 接下来，您需要编写代码来模拟UAC设备的行为。这涉及使用USB编程库，如libusb，来创建一个虚拟UAC设备并模拟音频输入和输出。

4. **配置UAC描述符：** UAC设备需要正确的USB描述符，以便与目标计算机正确通信。您需要配置这些描述符以确保设备被识别为UAC设备。

5. **实现音频流：** 您需要编写代码来处理音频数据的流动，包括音频输入和输出。这可能涉及音频采样、编码和解码，以及与USB传输的交互。

6. **加载驱动程序：** 一旦您编写了模拟UAC设备的代码，您需要将其编译并加载到树莓派上。您可能还需要配置udev规则以确保设备正确加载。

7. **连接到目标计算机：** 一旦您的树莓派被配置为UAC设备，您可以连接它到目标计算机的USB端口。

请注意，将树莓派配置为UAC设备是一个相对复杂的任务，需要深入的Linux系统和USB编程知识。如果您不熟悉这些领域，这可能会是一个具有挑战性的项目。在开始之前，建议研究相关的USB编程和树莓派的文档，并考虑寻求社区支持或咨询专业人员的帮助。

# xmos方案

XMOS 成立于2005年，主要设计用于物联网领域的高性能芯片，这些芯片可植入家用电器或是个人消费电子设备中。

市面上同类型的芯片产品并不少见，但 XMOS 处理器凭借着多核微控制器技术：**xCore**，该特性集 MCU、FPGA 和 DSP 特点于一身，在多种处理器中脱颖而出！

XMOS 这种特性带来的改变是，**以往一些需要采用 MCU、DSP 和低端 FPGA 三颗芯片的方案，现在只用一个 XMOS 就能全部完成。**

![img](images/random_name/v2-a64673eaf9115a8fac56a0370258ec58_720w.webp)

https://zhuanlan.zhihu.com/p/497360366

# uac驱动分析



https://www.cnblogs.com/wen123456/p/14281917.html

# UAC1.0和UAC2.0区别

传统3.5mm模拟耳机逐步被USB数字耳机代替。采用USB协议进行音频播放使用USB Audio Class协议(简称[UAC](https://www.usbzh.com/article/detail-80.html)).

[UAC](https://www.usbzh.com/article/detail-80.html)2.0由于支持USB High Speed，从而天生带有高带宽、低延时的优势。这些优势转化为对于Hi-Resolution Auido的支持。

[UAC](https://www.usbzh.com/article/detail-80.html)1.0最高只支持到双声道192Khz 16b的音源：(2 x 192 x 16) / 1024 = 6Mb = 6Mb/8 = 0.75MB

UAC2.0可以最高支持15声道384Khz 32b的音源：(15 x 384K x 32) /1024 = 180Mb = 18Mb/8 = 3MB



https://www.usbzh.com/article/detail-902.html



# UAC麦克风同步传输的URB分析

在[UAC](https://www.usbzh.com/article/detail-80.html)音频规范中，数据的传输不像UVC摄像头那样，既支持[同步传输](https://www.usbzh.com/article/detail-118.html)，也支持[批量传输](https://www.usbzh.com/article/detail-40.html)，

而是只支持同步传输。

所以[UAC](https://www.usbzh.com/article/detail-80.html)音频设备的数据端点都是同步端点。



USB总线比较复杂，并不是为音频传输特别设置的传输方式。

一个控制器通常需要对应多个设备，PC也有很多任务，其传输延迟会相对不那么稳定。



参考资料

1、

https://www.usbzh.com/article/detail-664.html

# UAC耳机扬声器音频写PCM数据的三种方式

[UAC](https://www.usbzh.com/article/detail-80.html)耳机扬声器音频PCM数据有三种方式，分别为：

- 异步传输 Asynchronous
- [同步传输](https://www.usbzh.com/article/detail-118.html) synchronous
- 自适应传输 adaptive。

## [UAC](https://www.usbzh.com/article/detail-80.html)音频数据[同步传输](https://www.usbzh.com/article/detail-118.html)

[同步传输](https://www.usbzh.com/article/detail-118.html)是三种方式中最低质量的，所以也是使用于一搬的普通产品中。同步传输时只要主机发送数据，设备端都会接收数据。==但由于两个时钟之间的误差，长时间工作会现音质下降的问题==。如破音，杂音等。不过一般人是听不出来的。哈哈

## 自适应传输 adaptive

自适应是设备不断调整其时钟的地方，以便它可以在发送数据时接受从计算机发送的数据。设备时钟的不断适应意味着设备中没有连续、准确的主时钟，这会导致音频流中的抖动。

## 异步传输 Asynchronous

这是最复杂的实现，但它是对其他类型的巨大改进。这是因为它要求数据包按照自己的时钟时序及时发送，从而提供最低的抖动和迄今为止最好的声音质量。



# UAC2驱动分析

UAC协议有UAC1.0和UAC2.0。UAC2.0协议相比UAC1.0协议，提供了更多的功能，支持更高的带宽，拥有更低的延迟。Linux内核中包含了UAC1.0和UAC2.0驱动，分别在f_uac1.c和f_uac2.c文件中实现。下面将以UAC2驱动为例，具体分析USB设备驱动的初始化、描述符配置、数据传输过程等。



https://blog.csdn.net/u011037593/article/details/121458492

# 参考资料

1、

https://blog.csdn.net/qianxuedegushi/article/details/113850337

2、

