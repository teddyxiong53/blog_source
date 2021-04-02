---
title: amlogic之A113L芯片
date: 2021-03-17 17:44:07
tags:
	- amlogic

---

A113L是低功耗的智能音视频soc。主打物联网应用。

Ultra-LowPowerSmartVoice/AudioProcessorfor IoTApplication

双核A35，带一个dsp（跑freertos）。

从后缀的L就可以看出，低功耗是主要卖点。

支持深度睡眠。

支持多阶段唤醒。

一个一直工作的vad模块。

一个2MB 的sram，用来给dsp做buffer。

集成了所有的标准video和audio接口。

2个内部adc给模拟mic用。

6个高动态范围的远场pdm数字mic接口。spdif接口。i2s接口。

音频输入数据可以被限制在可信内存范围。用来保护隐私。



# audio

## 音频接口

dailink有5个

```
0：tdma类型。
	对应的codec是dummy_codec。
1：i2s类型。
	tdmb。
	对应的codec是a1_codec
2：这个是pdm类型。
	对应的codc是pdm_codec。
3：spdif类型。
	也是dummy_codec。
4：loopback。
	也是dummy_codec。
	
```

toddr有3个：

vad、a、b

frddr有2个

a、b



loopback

loopback的输入是tdmin_lb，可以合入tdmin、spdif in、pdm in中的一个。



eqdrc

支持4个通道的。

只有2个通道同时支持eq和drc

另外2个，只支持eq。





参考资料

1、

