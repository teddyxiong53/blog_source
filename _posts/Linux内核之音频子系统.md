---
title: Linux内核之音频子系统
date: 2019-12-13 16:18:25
tags:
	- Linux内核

---

--

目前Linux中主流的音频体系结构是alsa。

alsa在驱动层提供了alsa-driver，在应用层提供了alsa-lib。

在Android里，没有使用标准的alsa，而是使用了简化版本的tinyalsa。但是在内核中仍然使用ALSA框架的驱动框架。

Android中使用tinyalsa控制管理所有模式的音频通路。

![img](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/2018070400313735)



![img](https://img-blog.csdn.net/20180706001400321?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTk2NTI3MA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)



4.1 Platform

           指某款soc平台的音频模块，比如qcom,omap,amlogic,atml等等。platform又可细分为二个部分：

cpu dai:

在嵌入式系统里面通常指soc的i2s,pcm总线控制器，

负责把音频数据从I2S tx FIFO搬运到codec(playback,capture则相反)。

cpu_dai通过 snd_soc_register_dai()来注册。

注：

DAI是Digital Audio Interface的简称，

分为cpu_dai和codec_dai,这两者通过i2s/pcm总线连接；

AIF是Audio Interface母的简称，嵌入式系统中一般是I2S和PCM接口。



PCM dma:

负责把dma buffer中的音频数据搬运到i2s tx fifo。

值得留意的是：

某些情形下是不需要dma操作的，

比如modem和codec直连，

因为modem本身已经把数据送到fifo了，

这时只需要启动codec_dai接收数据即可；

该情形下，machine驱动dai_link中需要设定.platform_name = "snd_soc_dummy",

这是虚拟dma驱动，实现见sound/soc/soc-utils.c. 

音频dma驱动通过 snd_soc_register_platform()来注册，

故也常用platform来指代音频dma驱动(这里的platform需要与soc platfrom区分开）。

Codec:

对于回放来说，userspace送过来的音频数据是经过采样量化的数字信号，

在codec经过DAC转换成模拟信号然后输出到外放或耳机，

这样我么你就可以听到声音了。

codec字面意思是编解码器，但芯片(codec)里面的功能部件很多，

常见的有AIF,DAC,ADC,Mixer,PGA,line-in,line-out，

有些高端的codec芯片还有EQ,DSP,SRC,DRC,AGC,Echo-Canceller,Noise-Suppression等部件。

比如本文中的npcp215x,自带Maxx算法。

Machine:

指某款机器，通过配置dai_link把cpu_dai,codec_dai,modem_dai各个音频接口给链结成一条条音频链路，

然后注册snd_soc_card.

和上面两个不一样，platform和codec驱动一般是可以重用的，

而machine有它特定的硬件特性，几乎是不可重用的。

所谓的硬件特性指：

Soc Platform与Codec的差异；DAIs之间的链结方式；通过某个GPIO打开Amplifier;通过某个GPIO检测耳机插拔；使用某个时钟如MCLK/External-OSC作为i2s,CODEC的时钟源等等。



![img](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/20180708144223271)



dai_link:

machine驱动中定义的音频数据链路，

它指定链路用到的codec,codec_dai,cpu_dai,platform.

比如对于amlogci这款，

通过dts来配置media链路：

codec ="npcp215x",codec-dai="npcp215x_e6",cpu_dai = "aml_tdmc",platform="aml-audio-card".

amlogic这款cpu通过dts来配置声卡的连接，

其相关解析和注册声卡都在soc/amlogic相关文件下。

.所以本文也会参考前言博主的的media链路：

codec="wm8994-codec",codec-dai="wm8994-aif1",cpu_dai="samsung-i2s",platform="samsung-audio",

这四者就构成了一条音频数据链路用于多媒体声音的回放和录制。

一个系统可能有多个音频数据链路，

比如media和voice,

因此可以定义多个dai_link.

如wm8994的典型设计，

有三个dai_link,分别是

API<>AIF1的"HIFI"(多媒体声音链路)，

BP<>AIF2的“voice”（通话语音链路），

以及BT<>AIF3(蓝牙sco语音链路)。



# 内核配置

要使用alsa，你至少需要使能CONFIG_SOUND。

因为alsa可以模拟oss。所以你可以不管oss。

这样使能alsa对oss的模拟

```
Enable "OSS API emulation" (CONFIG_SND_OSSEMUL)
```

![image-20201027101031080](../images/random_name/image-20201027101031080.png)

# ASOC

**asoc是为了给soc提供更好的alsa支持。**

在引入asoc之前，存在的问题：

1、codec驱动给特定的soc紧密耦合。导致了代码重复。例如wb8731这个codec芯片，对于不同的soc，需要多份代码。

2、没有标准的方法来发送音频event信号。例如耳机检测

3、驱动一般使能整个codec，即使只是播放音频。这个不利于降低功耗。

针对上面的问题，就提出了asoc架构。

asoc有如下特点：

1、codec完全独立。这样就便于复用codec驱动代码。

2、在codec和soc之间建立I2S/PCM接口很容易。

3、动态audio功耗管理。在任何时候，只使能需要的功能。

4、机器特定控制支持。

为了实现上面这些目标。asoc把系统分为下面几个组件：

1、codec 类driver。平台独立，包含音频控制，音频接口，还可以支持FM/BT。

2、platform 类driver。包括DAI驱动等。

3、machine类driver。

## codec

### codec类驱动

每一个codec类驱动应该提供：

1、DAI 和PCM配置。

2、io控制，使用regmap api。

3、mixer和audio控制。

4、audio操作。

5、动态功耗描述。

6、动态功耗事件处理。

7、mute控制。这个可选。

跟sound/soc/codecs目录下的文件结合一起看。

**每一个codec驱动，都必须有一个snd_soc_dai_driver结构体**，来描述DAI和PCM能力和操作。

这个结构体对外暴露，**这样你的machine driver就可以把这个codec driver注册到系统。**

举例：

```
static struct snd_soc_dai_ops wm8731_dai_ops = {
	.prepare	= wm8731_pcm_prepare,
	.hw_params	= wm8731_hw_params,
	.shutdown	= wm8731_shutdown,
	.digital_mute	= wm8731_mute,
	.set_sysclk	= wm8731_set_dai_sysclk,
	.set_fmt	= wm8731_set_dai_fmt,
};

struct snd_soc_dai_driver wm8731_dai = {
	.name = "wm8731-hifi",
	.playback = {
		.stream_name = "Playback",
		.channels_min = 1,
		.channels_max = 2,
		.rates = WM8731_RATES,
		.formats = WM8731_FORMATS,},
	.capture = {
		.stream_name = "Capture",
		.channels_min = 1,
		.channels_max = 2,
		.rates = WM8731_RATES,
		.formats = WM8731_FORMATS,},
	.ops = &wm8731_dai_ops,
	.symmetric_rates = 1,
};

```

codec一般的通过spi或者i2c来进行控制的。

**AC97接口特殊一些，它的控制信号也是走数据通路的。**

**统一用regmap来传递控制信号。**

AC97是5线接口。在PC上用的多。

I2S和PCM对比

I2S：4线。Rx、Tx、bclk（bit clock）、LRC（Left/Right Clock）

PCM：也是4线。跟I2S很像。就是有一根线是sync（I2S是LRC）。其余3根一样。

PCM有两种模式：

模式A：下降沿传输。

模式B：上升沿传输。

#### 以adc3101为例分析

天猫精灵X1

德州仪器的型号为TAS5751M的数字音频功率放大器

背面还有一颗S0903的灯控芯片。

该麦克风阵列由思必驰提供，而模拟麦克风则来自敏芯微电子。该电路板上还有4块德州仪器型号为TLV320ADC3101低功耗立体声ADC(模数变换器)。此外，还有一块A1semi的型号为AS9050D的触摸控制器。



在S400的板子上，有一颗CS4354的ADC芯片。连接到line out端口。

https://www.cn.cirrus.com/products/cs4354/

输入这个是接到了soc的I2S引脚上。



年度盘点：6款内置晶晨方案智能音箱拆解汇总

https://www.52audio.com/archives/15302.html



### mixer和control

所有的mixer和control，都可以用soc.h里的这个宏来定义

```
#define SOC_SINGLE(xname, reg, shift, mask, invert)
```

xname：mixer的名字，例如“Playback volume”

reg：codec的寄存器。

shift：寄存器里的bit位移。

mask：控制的bit的mask。例如7表示3个bit。

invert：是否invert。

还有其他几个类似的宏。

### codec audio ops

对应结构体struct snd_soc_ops 

```

```

## dai

dai是数字音频接口的缩写。

asoc现在支持3个主要的dai：ac97、i2s、pcm。

## platform

asoc platform driver可以分为：

1、audio dma driver。

2、soc dai driver。

3、dsp driver。

platform driver必须跟cpu相关，不跟具体的board相关。

## machine

asoc machine driver是把codec driver、platform、dai这些驱动粘合到一起的驱动。

对应的结构体是snd_soc_card。



对于目前嵌入式系统上的声卡驱动开发，我们建议读者尽量采用 ASoC 框架， ASoC 主要
由 3 部分组成。

Codec 驱动。这一部分只关心 Codec 本身，与 CPU 平台相关的特性不由此部分操作。
平台驱动。这一部分只关心 CPU 本身，不关心 Codec。它主要处理两个问题： DMA 引擎和 SoC 集成的 PCM、 I2S 或 AC ‘97 数字接口控制。

板驱动（也称为 machine 驱动）。这一部分将平台驱动和 Codec 驱动绑定在一起，描述了板一级的硬件特征。



在以上 3 部分中， 1 和 2 基本都可以仍然是通用的驱动了，

也就是说， Codec 驱动认为自己可以连接任意 CPU，

而 CPU 的 I2S、 PCM 或 AC ‘97 接口对应的平台驱动则认为自己可以连接任
意符合其接口类型的 Codec，

只有 3 是不通用的，

由特定的电路板上具体的 CPU 和 Codec 确定，

**因此它很像一个插座，上面插上了 Codec 和平台这两个插头。**

**在以上三部分之上的是 ASoC 核心层，**

由内核源代码中的 sound/soc/soc-core.c 实现，

查看其源代码发现它完全是一个传统的 ALSA 驱动。

因此，对于基于 ASoC 架构的声卡驱动而言， alsa-lib以及 ALSA 的一系列 utility 仍然是可用的，

如 amixer、 aplay 均无需针对 ASoC 进行任何改动。

而ASoC 的用户编程方法也与 ALSA 完全一致。





由上图我们可以看出，3.0中的数据结构更为合理和清晰，

取消了snd_soc_device结构，

直接用snd_soc_card取代了它，

并且强化了snd_soc_pcm_runtime的作用，

同时还增加了另外两个数据结构snd_soc_codec_driver和snd_soc_platform_driver，

用于明确代表Codec驱动和Platform驱动。



# 音频相关参数



# 参考资料

1、linux驱动由浅入深系列：tinyalsa(tinymix/tinycap/tinyplay/tinypcminfo)音频子系统之一

https://blog.csdn.net/radianceblau/article/details/64125411

2、Documentation/sound/alsa目录下的文档

3、

https://blog.csdn.net/syh63053767/article/details/9126869

4、Linux音频子系统

这个是系列，但是分析的是2.6版本的，太老了。

https://blog.csdn.net/droidphone/category_1118446.html

这个比较新。

https://blog.csdn.net/vertor11/article/details/79211719

5、

https://blog.csdn.net/moonlinux20704/article/details/88417361

6、Linux ALSA音频系统:platform,machine,codec

https://blog.csdn.net/wenjin359/article/details/83002041

7、音频相关参数的记录（MCLK、BCLK、256fs等等）

https://blog.csdn.net/lugandong/article/details/72468831