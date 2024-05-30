---
title: 蓝牙之音频sbc编码
date: 2019-03-08 14:54:11
tags:
	- 蓝牙

---

--

我们手机连接蓝牙耳机听歌，手机上的音频经过编码后通过蓝牙协议被蓝牙耳机接收。

经过解码之后，蓝牙耳机成功获取手机上的音频信息，然后再转化为震动被人耳识别。

**这个是一个典型的数字通信系统。**

对于蓝牙耳机来说，信源就是pcm数据。

sbc编码跟aac、mp3是一个类型的东西。

**sbc编码是蓝牙协议规定的，所有的蓝牙设备都必须支持。**

蓝牙SBC算法是一种以中等比特率传递高质量音频数据的低计算复杂度的音频编码算法

# 简介

SBC（Low Complexity Subband Coding）是一种基于子带的音频编码器，通常用于蓝牙音频传输。它是蓝牙A2DP（Advanced Audio Distribution Profile）标准中所采用的默认音频编解码器之一。

SBC编码器的主要特点和工作原理包括：

1. **压缩算法：** SBC使用子带的方法对音频进行压缩。它将音频信号分成多个频带，并对每个频带进行编码，从而在一定程度上减小了数据量。

2. **可调的参数：** SBC允许根据传输要求和设备性能进行参数调整，包括比特率、声道模式、子带数等，以平衡音频质量和传输效率。

3. **多种声道模式：** SBC支持多种声道模式，例如单声道、立体声、联合立体声等，允许选择合适的声道模式以适应不同的音频源。

4. **广泛兼容性：** 由于是A2DP标准的一部分，SBC编码器几乎兼容所有支持A2DP的蓝牙音频设备。

SBC编码器的主要优势在于其普遍性和兼容性，几乎所有的蓝牙音频设备都支持SBC，这使得它成为了蓝牙音频传输中的默认编码器。然而，由于其相对较低的编码效率，有时可能会导致音频质量不如一些更高级的编解码器，例如aptX或者LDAC。



# sbc编码原理

sbc是SubBand Codec。次频带编码。

也叫子带编码。

**基本原理是把信号的频率分为若干个子带，然后对每个子带进行编码。**

然后根据每个子带的重要性，给不同的精度。这样就区分了重点。

主要是人耳对不同频率的敏感性不一样。这个是理论基础。



只支持这4种采样率。

```
#define SBC_SAMPLING_FREQ_16000		(1 << 3)
#define SBC_SAMPLING_FREQ_32000		(1 << 2)
#define SBC_SAMPLING_FREQ_44100		(1 << 1)
#define SBC_SAMPLING_FREQ_48000		1
```

# 代码

https://github.com/pschatzmann/arduino-audio-tools/wiki/Encoding-and-Decoding-of-Audio

https://github.com/pschatzmann/arduino-libsbc





# 参考资料

1、蓝牙协议中的SBC编码

https://www.cnblogs.com/huahuahu/p/lan-ya-xie-yi-zhong-deSBC-bian-ma.html

2、

https://www.rtings.com/headphones/learn/sbc-aptx-which-bluetooth-codec-is-the-best

3、SBC音频编解码算法浅析

https://blog.csdn.net/ceetoo/article/details/80270574