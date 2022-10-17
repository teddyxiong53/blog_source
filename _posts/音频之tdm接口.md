---
title: 音频之tdm接口
date: 2021-03-26 10:46:41
tags:
	- 音频

---

--

tdm：就是时分复用调制的缩写。

![在这里插入图片描述](../images/random_name/20210209153656910.png)

有些IC支持使用一个公共时钟的多路I2S数据输入或输出，

但这样的方法显然会增加数据传输所需要的管脚数量。

**当同一个数据线上传输两个以上通道的数据时，就要使用TDM格式。**

TDM数据流可以承载多达16通道的数据，并有一个类似于I2S的数据/时钟结构。



**每个通道的数据都使用数据总线上的一个槽（Slot），**

其宽度相当于帧的1/N， 其中N是传输通道的数量。

出于实用考虑，N通常四舍五入到最近的2次幂（2、4、8、或16），

**并且任何多余通道都被空闲。**

一个TDM帧时钟通常实现为一位宽的脉冲，

这与I2S的50%占空比时钟相反。

**超过25 MHz的时钟速率通常不用于TDM数据，**

原因是较高的频率会引起印刷电路板设计者要避免的板面布局问题。



TDM常用于多个源馈入一个输入端，

或单源驱动多只器件的系统。

在前一种情况下，（多源馈入一个输入端），

每个TDM源共享一个公共的数据总线。

该信源必须配置为在其适用通道期间才驱动总线，

而当其它器件在驱动其它总线时，其驱动器要置为三态。



**TDM接口还没出现类似飞利浦I2S的其他标准，**

因此，很多IC都有着自己略微不同的TDM实现方法。

这些变化体现在时钟极性、通道配置，以及闲置通道的三态化和驱动上。

当然，通常情况下不同IC是可以一起工作的，

但系统设计者必须确保一个器件的输出格式要符合另一只器件输入端的预期



**PDM数据连接**

PDM数据连接在手机和平板电脑等**便携音频应用**上方面变得越来越普遍。

PDM在尺寸受限应用中优势明显，

因为它可以将音频信号的布放围绕LCD显示屏等高噪声电路，

而不必处理模拟音频信号可能面临的干扰问题。



有了PDM，仅两根信号线就可以传输两个音频通道。

如图4系统框图所示，

两个PDM源将一根公共数据线驱动为一个接收器。

系统主控生成一个可被两个从设备使用的时钟，

这两个从设备交替使用时钟的边缘，

通过一根公共信号线将其数据输出出去。



TDM相比I2S 可以传输多ch音频数据，分为2种模式:dsp_a 和dsp_b

![img](../images/playopenwrt_pic/20210623154352113.png)



PCM数字音频接口，

即说明接口上传输的音频数据通过PCM方式采样得到的，

以区别于PDM方式。

在音频领域，PCM接口常用于板级音频数字信号的传输，与I2S相似。

PCM和I2S的区别于数据相对于帧时钟（FSYNC/WS）的位置、时钟的极性和帧的长度。

**其实，I2S上传输的也是PCM类型的数据，因此可以说I2S不过是PCM接口的特例。**



相比于I2S接口，PCM接口应用更加灵活。

通过时分复用（TDM, Time Division Multiplexing）方式，

PCM接口支持同时传输多达N个（N>8）声道的数据，

**减少了管脚数目（实际上是减少I2S的“组”数，因为每组I2S只能传输两声道数据嘛）。**

TDM不像I2S有统一的标准，不同的IC厂商在应用TDM时可能略有差异，

这些差异表现在时钟的极性、声道配置的触发条件和对闲置声道的处理等。



综合不少厂商的数据手册，笔者发现，在应用PCM音频接口传输单声道数据（如麦克风）时，其接口名称为***PCM\***；双声道经常使用***I2S\***；而***TDM\***则表示传输两个及以上声道的数据，同时区别于I2S特定的格式。



在实际应用中，总是以帧同步时钟FSYNC的上升沿表示一次传输的开始。帧同步时钟的频率总是等于音频的采样率，比如44.1 kHz，48 kHz等。多数应用只用到FSYNC的上升沿，而忽略其下降沿。根据不同应用FSYNC[脉冲宽度](https://www.zhihu.com/search?q=脉冲宽度&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A373060896})的差别，PCM帧同步时钟模式大致分为两种：

- **长帧同步** Long Frame Sync
- **短帧同步** Short Frame Sync

# 设备树配置相关

最近配置amlogic的tdm接口，发现这个还比较复杂。需要通过多读文章来加深理解。

比如我们要配置一个12.288MHz，BCLK的TDM总线， **WS/LRCK**一般都是配置48Khz，位深度是32 bit，然后有8个声道，计算起来**SCLK/BCLK**就是12.288MHz。

```

 12.288 MHz =  48 kHz * 32 bits per slot * 8 slots/channels
```

改了之后用示波器抓波形，然后执行以下tinyalsa命令使得总线工作：

```cpp
tinymix "MultiMedia1 Mixer SEN_TDM_TX_0" "1"
```



# tdm和i2s区别

```
I need to receive 8 channels of 24 bits at 48KHz. So I have two possibilities to accomplish that: either using 4 I2S or TDM.

I would like to understand the difference in clock rates between I2S and TDM. For example: in TDM mode the bit rate is 24 x 48KHz x 8 = 9.216 Mbps. In I2S mode the bit rate is slower once it transmits just two channels : 24 x 48KHz x 2 = 2.304 Mbps.
```



https://electronics.stackexchange.com/questions/601569/multi-channel-i2s-vs-tdm



# 参考资料

1、TDM格式介绍 - 音频数据传输的常见IC间数字接口介绍

http://www.elecfans.com/video/yinpinjishu/20121210301406_2.html

2、

http://www.wangdali.net/wp-content/uploads/2014/10/%E6%95%B0%E5%AD%97%E9%9F%B3%E9%A2%91%E6%8E%A5%E5%8F%A3.pdf

3、数字音频接口之TDM

https://blog.csdn.net/songche123/article/details/118154829

4、TDM协议

https://zhuanlan.zhihu.com/p/373060896

5、

https://blog.csdn.net/Codeliang666/article/details/113859859