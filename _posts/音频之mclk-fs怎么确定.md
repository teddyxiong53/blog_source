---
title: 音频之mclk-fs怎么确定
date: 2021-12-09 10:59:25
tags:
	- 音频

---

--

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



# 参考资料

1、

https://blog.csdn.net/lugandong/article/details/72468831

2、

https://www.cnblogs.com/blogs-of-lxl/p/14722603.html

3、音频相关参数的记录（MCLK、BCLK、256fs等等）

https://blog.csdn.net/hanmengaidudu/article/details/88868919