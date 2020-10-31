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

asoc是为了给soc提供更好的alsa支持。

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

## codec类驱动

每一个codec类驱动应该提供：

1、DAI 和PCM配置。

2、io控制，使用regmap api。

3、mixer和audio控制。

4、audio操作。

5、动态功耗描述。

6、动态功耗事件处理。

7、mute控制。这个可选。

跟sound/soc/codecs目录下的文件结合一起看。

每一个codec驱动，都必须有一个snd_soc_dai_driver结构体，来描述DAI和PCM能力和操作。

这个结构体对外暴露，这样你的machine driver就可以把这个codec driver注册到系统。

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

AC97接口特殊一些，它的控制信号也是走数据通路的。

统一用regmap来传递控制信号。

AC97是5线接口。在PC上用的多。

I2S和PCM对比

I2S：4线。Rx、Tx、bclk（bit clock）、LRC（Left/Right Clock）

PCM：也是4线。跟I2S很像。就是有一根线是sync（I2S是LRC）。其余3根一样。

PCM有两种模式：

模式A：下降沿传输。

模式B：上升沿传输。



参考资料

1、linux驱动由浅入深系列：tinyalsa(tinymix/tinycap/tinyplay/tinypcminfo)音频子系统之一

https://blog.csdn.net/radianceblau/article/details/64125411

2、Documentation/sound/alsa目录下的文档