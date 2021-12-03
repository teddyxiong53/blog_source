---
title: 音频之i2s的mclk、bclk、sclk
date: 2021-12-02 16:36:33
tags:
	- 音频

---

--

拿512fs说话：
看图知道采样的位深是32bit（位），左右声道各占了8*32BCLK，那一个完整的LRCLK一共8*32*2=512BCLK。
其实xxxfs就是这么算出来的，也是固定的，当你定了几个channel，多少位深，就几乎可以确认是多少fs了。从主观的角度来看，fs的数值越大，那么一个完整的LRCLK越多，那承载的数据量就越大，随之的就是音质就会更加好。
fs是freq sample的意思吧。



mclk：soc提供给外部设备的系统时钟；

Bclk(sclk)：串行位时钟，每个cycle代表一次采样，频率与通道数\通道宽度\采样率相关；

Lrclk（fclk）：左右声道时钟或帧时钟，每个cycle代表一个frame，频率等于采样率；

SD：serial data line，传输音频数据；



Soc master\codec slave模式下：bclk\lrclk由soc提供，playback时soc通过dataline传输数据，codec采样；capture时codec通过dataline传输数据，soc采样；

Soc slave\codec master模式下：soc向codec提供mclk，bclk\lrclk由codec提供；



参考资料

1、

https://blog.csdn.net/lugandong/article/details/72468831