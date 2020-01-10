---
title: Linux之耳机线插入检测
date: 2020-01-07 10:53:08
tags:
	- Linux

---

1

耳机线插入，也属于input子系统的一部分。

对应switch event。

是SW_HEADPHONE_INSERT事件。

在sound/core/jack.c里，定义了耳机等jack设备。



audio jack（就是3.5mm接口）一般有switch用来做插入检测的。

大多数的codec芯片都可以实现jack检测。



在rk3308的sdk的《Rockchip Audio开发指南》里，有这样一句话：

```
JACK:耳机的接口检测，大部分使用 Codec 自身的检测机制，小部分使用 IO来进行模拟
```

一个声卡包括

cpu_dai：对应cpu_dai的driver，例如i2s driver，spdif driver

codec_dai：对应codec driver，例如rt5640 codec driver

dai_link：对应dai_link driver。也就是machine driver。比如sound/soc/rockchip/rockchip_rt5640.c。



4.4的内核支持两种方式创建声卡。

1、使用通用的simple-card framework。建议优先考虑这种。

2、传统的编写自定义的machine driver的方式。



瑞芯微RK3308是全新针对音频应用的方案，省去了GPU、视频编解码以及显示输出等部分，**增加了CODEC以及音频相关模块**，不论是芯片成本还是系统成本都进行了优化，实现超高性价比。

内置音频高性能CODEC（8通道 ADC + 2通道 DAC）

直接支持最大8通道模拟MIC阵列+回采，无需外加ADC

为低功耗应用开发了硬件语音检测模块（VAD）

http://www.ruiyixi.com/project/an-rk3308-pcba-for-ai-and-iot/



参考资料

1、耳机插入检测学习总结

https://wenku.baidu.com/view/7435b1eef18583d048645904.html

2、RK android带MIC耳机检测以及hook-kernel

这个很游泳。

https://wenku.baidu.com/view/21f06b66bfd5b9f3f90f76c66137ee06eef94e01.html?from=search