---
title: 音频之spdif接口
date: 2021-03-26 11:10:41 
tags:
	- 音频

---

--

# 简介

spdif是sony和Philips合作开发的接口。

缩写里的d表示digital。

就传输方式而言，SPDIF分为输出（SPDIF OUT）和输入（SPDIF IN）两种。

**大多数的声卡芯片都能够支持SPDIF OUT，**

但我们需要注意，并不是每一种产品都会提供数码接口。

**而支持SPDIF IN的声卡芯片则相对少一些，**

如：EMU10K1、YMF-744和FM801-AU、CMI8738等。

SPDIF IN在声卡上的典型应用就是CD SPDIF，但也并不是每一种支持SPDIF IN的[声卡](https://baike.baidu.com/item/声卡/108520)都提供这个接口。



就传输载体而言，**SPDIF又分为同轴和光纤两种**，

其实他们可传输的信号是相同的，只不过是载体不同，接口和连线外观也有差异。

**但光信号传输是今后流行的趋势，**

其主要优势在于无需考虑接口电平及阻抗问题，

接口灵活且抗干扰能力更强。

**通过SPDIF接口传输数码声音信号已经成为了新一代PCI声卡普遍拥有的特点。**



# **数字音箱与数字声卡的关系**

其次大家可能对依靠同轴SPDIF OUT连接[数字式音箱](https://baike.baidu.com/item/数字式音箱)从而实现纯[数字音频](https://baike.baidu.com/item/数字音频)回放的具体原理不太清楚，

接下来笔者为大家简要介绍一下。

前面我们就提到过，声卡的[数字模拟转换](https://baike.baidu.com/item/数字模拟转换/18451742)工作是交给CODEC芯片来完成的。

但是我们的[电脑机箱](https://baike.baidu.com/item/电脑机箱)内依然存在着严重的电磁波，

**D/A、A/D转换仍然会受到比较严重的信号干扰。**

许多专业音频录音卡普遍采用将CODEC外置的做法，

把数模转换部分以及各类外部接口等单独做成一个外置盒，以提高音质。

但是这样做的直接后果便是成本大幅度提高，在家用多媒体市场肯定是曲高和寡的。

那到底有没有价廉物美的办法呢？

**一些音箱厂家就想出了把D/A转换工作从声卡上转移到音箱上的方案，**

数字式多媒体音箱也就应运而生了，

CREATIVE的FPS2000 Digital、Sound Works 2.1Digital就属于这种类型。

这种方案的基本原理就是声音信号不经过声卡CODEC芯片的转换处理，

**直接以PCM格式，使用声卡上的同轴SPDIF OUT，**

以纯数字方式传输到数字音箱中，

通过音箱内置的[D/A转换器](https://baike.baidu.com/item/D%2FA转换器)解码，随后放大输出。

**这样干扰减小了，信噪比自然有所提高。**

主要不足之处在于，眼下部分数字音箱的D/A转换单元、放大器、扬声器素质不高，造成数字式传输的优势不能被完美的表现出来。



spdif上传输pcm格式数字音频。**数字的抗干扰能力比模拟信号好得多。**

传输容易受到干扰。

# spdif信号

S/PDIF往往被用来传输压缩过的音频讯号，它由 IEC 61937标准而定制。

spdif发出的波形为BMC编码，时钟与数据混合在一起进行编码。

# 参考资料

1、SPDIF

https://baike.baidu.com/item/SPDIF/7208010?fr=aladdin

2、

https://www.touying.com/t-43734-1.html

3、

https://blog.csdn.net/CallMe_Xu/article/details/120533677