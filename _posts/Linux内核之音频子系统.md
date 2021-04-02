---
title: Linux内核之音频子系统
date: 2019-12-13 16:18:25
tags:
	- Linux内核

---

1

目前Linux中主流的音频体系结构是alsa。

alsa在驱动层提供了alsa-driver，在应用层提供了alsa-lib。

在Android里，没有使用标准的alsa，而是使用了简化版本的tinyalsa。但是在内核中仍然使用ALSA框架的驱动框架。

Android中使用tinyalsa控制管理所有模式的音频通路。



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