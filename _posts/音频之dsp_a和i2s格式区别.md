---
title: 音频之dsp_a和i2s格式区别
date: 2021-12-09 10:56:25
tags:
	- 音频

---

--

PCM/DSP mode分为Mode-A和Mode-B共2种模式。不同芯片的datasheet中有的称为PCM mode；有的称为DSP mode。

I2S mode分为标准i2s-standard mode (也成为philips飞利浦标准)，i2s-MSB-Left-justified mode，i2s-MSB-Right-justified mode共三种模式。



# tdm接口上 i2s格式和dsp_a格式的区别

在 TDM（Time-Division Multiplexing）接口上，I2S 格式和 DSP_A 格式是两种不同的音频数据传输格式。

1. I2S 格式（Inter-IC Sound）是一种常见的音频传输格式，通常用于数字音频设备之间的数据传输。它采用左右声道分离、同步的方式传输音频数据。I2S 格式的数据包含三个信号线：位时钟（BCLK）、帧同步（LRCLK）和数据线（DATA）。位时钟用于定时采样和数据传输的同步，帧同步用于标识每个音频帧的开始，数据线传输音频采样值。I2S 格式常用于连接音频芯片、CODEC（编解码器）、DSP（数字信号处理器）等设备。

2. DSP_A 格式是一种特定的 TDM 接口数据格式，主要用于连接 AMLogic 系统芯片和音频处理器之间的数据传输。它采用了 AMLogic 独有的数据帧结构和时钟分配方式。DSP_A 格式的数据帧包含多个时隙（Slots），每个时隙传输一个音频通道的数据。不同于 I2S 格式的左右声道分离，DSP_A 格式将多个音频通道的数据依次放置在不同的时隙中。时隙的数量和宽度可以根据具体需求进行配置。DSP_A 格式在 AMLogic 系统中广泛应用于音频处理和音频传输。

总结来说，I2S 格式是一种通用的音频传输格式，适用于各种音频设备的连接。而 DSP_A 格式是 AMLogic 系统特定的 TDM 接口数据格式，用于连接 AMLogic 芯片和音频处理器。两者在数据帧结构和时钟分配方式上有所差异，因此在具体应用中需要根据系统需求选择合适的格式。

# 参考资料

1、

https://blog.csdn.net/qingfengjuechen/article/details/104696568