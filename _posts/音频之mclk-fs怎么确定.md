---
title: 音频之mclk-fs怎么确定
date: 2021-12-09 10:59:25
tags:
	- 音频

---

--

fs的频率选择的意思。

mclk-fs=256的意思是，mclk的频率是采样率的256倍。



```
看图知道采样的位深是32bit（位），左右声道各占了8*32BCLK，那一个完整的LRCLK一共8*32*2=512BCLK。 
其实xxxfs就是这么算出来的，也是固定的，当你定了几个channel，多少位深，就几乎可以确认是多少fs了。从主观的角度来看，fs的数值越大，那么一个完整的LRCLK越多，那承载的数据量就越大，随之的就是音质就会更加好。
```



```
上图是32位的采样，2channel，xxxfs的选择有： 
128fs、256fs、512fs

如果是16bit的采样，2channel呢？ 
16*2（channel）*2（每个LR有几个16BCLK组成） = 64fs 
按照倍数的增加，会有如下的选择： 
64fs、128fs、256fs、512fs

如果是24bit的采样，2channel呢？ 
24*2（channel）*2（每个LR有几个16BCLK组成） = 96fs 
按照倍数的增加，会有如下的选择： 
96fs、192fs、384fs、768fs（这个级别的估计一般的ADC很难）
```



拿512fs说话：
看图知道采样的位深是32bit（位），左右声道各占了`8*32BCLK`，那一个完整的LRCLK一共`8*32*2=512BCLK`。
其实xxxfs就是这么算出来的，也是固定的，当你定了几个channel，多少位深，就几乎可以确认是多少fs了。从主观的角度来看，fs的数值越大，那么一个完整的LRCLK越多，那承载的数据量就越大，随之的就是音质就会更加好。
fs是freq sample的意思吧。



mclk：soc提供给外部设备的系统时钟；

Bclk(sclk)：串行位时钟，每个cycle代表一次采样，频率与通道数\通道宽度\采样率相关；

Lrclk（fclk）：左右声道时钟或帧时钟，每个cycle代表一个frame，频率等于采样率；

SD：serial data line，传输音频数据；



Soc master\codec slave模式下：

bclk\lrclk由soc提供，

playback时soc通过dataline传输数据，codec采样；

capture时codec通过dataline传输数据，soc采样；



Soc slave\codec master模式下：

**soc向codec提供mclk，**

**bclk\lrclk由codec提供；**



另外I2S只能传2个声道的数据，

**PCM可以传多达16路数据，采用时分复用的方式，就是TDM。**

像现在最流行的语音智能音箱的7麦克风矩阵，一般都是用TDM来传的数据，同时可以传输7路麦克风输入和3路以上的音频反馈信号。

**AP处理器和蓝牙之间也是通过PCM来传输语音数据，打电话的蓝牙数据走的是PCM，放音乐的蓝牙数据走的是串口（不是PCM）。**

**TDM**: 包括PCM format 和 I2S format，下图是TDM-I2S Mode, 在I2S format下传输多channel。



鉴于如上的，那它是xxxfs？ 
正常是fs=MCLK/ sample_rate=5.6448*1000/44.1=128fs

`fs=16*2*（LRCLK各几个16 BCLK组）=128fs`，一共是4个。

# i2s的mclk、bclk、lrclk关系

在I2S（Inter-IC Sound）接口中，MCLK（Master Clock）、BCLK（Bit Clock）和LRCLK（Left/Right Clock）是三个重要的时钟信号，它们之间存在以下关系：

1. MCLK（Master Clock）是I2S接口的主时钟信号，它提供了整个音频系统的时钟同步。MCLK的频率通常由音频设备的主设备（例如主控芯片）提供，并且是I2S接口中最高频率的时钟。MCLK的频率可以根据系统需求而变化，常见的频率有12.288 MHz、22.5792 MHz、24.576 MHz等。

2. BCLK（Bit Clock）是用于同步音频数据的时钟信号。它确定每个音频样本的位数和传输速率。BCLK的频率是由MCLK的频率除以每个样本的位数得出的，通常为MCLK频率的几分之一。例如，**对于16位音频样本，BCLK的频率将是MCLK频率的1/32。**BCLK的边沿用于将音频数据从发送器（transmitter）传输到接收器（receiver）。

3. LRCLK（Left/Right Clock）是用于指示音频数据通道的时钟信号。它确定了音频样本是左声道还是右声道数据。**LRCLK的频率是BCLK频率的一半，因为每个音频样本通常由左声道数据和右声道数据交替传输。**当LRCLK为高电平时，表示传输的是左声道数据；当LRCLK为低电平时，表示传输的是右声道数据。

综上所述，MCLK提供了整个音频系统的主时钟，BCLK用于同步音频数据的传输速率，而LRCLK用于指示音频数据的通道。它们之间的频率关系是通过MCLK和每个音频样本的位数来确定的。正确的时钟同步和频率设置对于正确的音频数据传输和解码至关重要。

# mclk pad select

"MCLK pad select" 是一个配置选项，用于选择特定的 MCLK（主时钟）引脚。

在一些设备或芯片中，存在多个 MCLK 引脚可用于连接外部主时钟信号。这些 MCLK 引脚通常具有不同的功能和特性，例如频率范围、电压等。通过 "MCLK pad select" 配置选项，可以选择将外部主时钟信号连接到特定的 MCLK 引脚上，以满足系统设计和需求。

选择适当的 MCLK 引脚可以确保与外部主时钟信号的正确连接，并确保所需的时钟频率和电气特性得到满足。这通常在设备树或硬件配置文件中进行配置，以便在系统初始化过程中正确地将外部主时钟信号引导到所选的 MCLK 引脚上。

具体的 MCLK pad select 配置选项和可用的引脚可能因芯片厂商和设备设计而有所不同，需要参考相关的技术文档和硬件规格来了解具体的配置和使用方式。

# 参考资料

1、

https://blog.csdn.net/lugandong/article/details/72468831

2、

https://www.cnblogs.com/blogs-of-lxl/p/14722603.html

3、音频相关参数的记录（MCLK、BCLK、256fs等等）

https://blog.csdn.net/hanmengaidudu/article/details/88868919