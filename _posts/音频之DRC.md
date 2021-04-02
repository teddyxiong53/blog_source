---
title: 音频之DRC
date: 2020-04-06 10:10:51
tags:
	- 音频

---

1

DRC，全称是Dynamic Range Compress。动态范围压缩。

主要的作用是限制喇叭的功率输出。

简单的讲，DRC可以帮助我们设定比较大的增益放大小信号，大信号时又不失真。

不失真的提升平均音量，此功能还可以保护喇叭。

如果没有DRC，音量控制相对比较尴尬，音量过大会使大信号音源经放大后失真；音量过小会导致小信号音源的时候整体输出音量不够。

rk3308的方案里，有一个eq_drc_process进程。

启动脚本是这样：

```
aplay -D softvol /oem/silence.wav
/oem/acodec-gain.sh &
export EQ_LOW_POWERMODE=true
export PLAYBACK_HPF_PASS=0hz
case "$1" in
	start)
		# ueventd
		cp -rf /etc/presetFile.sat /data/presetFile.sat
		sleep 1
		/usr/bin/eq_drc_process &
		;;
```



acodec-gain.sh 这个脚本的内容：

这个没有什么内容，就是用amixer设置一下Master的音量。



ＥQ英文全称Equaliser，中文也就是均衡器的意思。

它的基本作用是通过对声音**某一个或多个频段进行增益或衰减**，

从而达到调整音色的目的。

EQ通常包括以下三个参数：

Frequency，频率――这是用于设定你要进行调整的频率点的参数；

Gain，增益――用于调整在你设定好的F值上进行增益或衰减的参数；

Quantize，频宽比――用于设定你要进行增益或衰减的频段“宽度”的参数。Q值越小处理的频段就越宽。



应用角度说明：

音乐均衡器有两种常见类型，

一种是图示均衡器（Graphic Equalizer），

另一种是参量均衡器（Parametric Equalizer）。



图示均衡器是一种按照一定的规律把全音频20～20000 Hz划分为若干的频段，

每个频段对应一个可以对电平进行增益或衰减的调节器，

可以根据需要，对输入的音频信号按照特定的频段进行单独的增益或衰减。



参量均衡器不划分固定的波段，

可对任意一个频率点（包括频点附近指定频率带宽内的所有点）进行控制，

通过调整带宽，使得调节控制可精确（小带宽），也可模糊（大带宽），非常灵活。



参量均衡器操作控制不直观，

多用在对声音精确控制的专业场合。

而像Winamp和Foobar这样的音频播放器，

多采用图示均衡器，

通过一个带调节器的图形面板可以让用户很方便地对特定频段进行调节。



信号形态角度说明：

均衡器又可以分为

时域均衡器

和频域均衡器

两种类型。



时域均衡器对时域音频信号

通过叠加一系列滤波器实现对音色的改变，

无论是传统的音响设备还是众多音乐播放软件，绝大多数都是使用时域均衡器。

时域均衡器通常由一系列二次IIR滤波器或FIR滤波器串联组合而成，

每个波段对应一个滤波器，各个滤波器可以单独调节，

串联在一起形成最终的效果。

但是，传统的IIR滤波器具有反馈回路，会出现相位偏差，

而FIR滤波器会造成比较大的时间延迟。

另外，如果使用IIR或者FIR滤波器，均衡器波段越多，需要串联的滤波器的个数也越多，运算量也越大。



频域均衡器

是在频域内直接对指定频率的音频信号进行增益或衰减，

从而达到改变音色的目的。频域均衡器没有相位误差和时间延迟，而且不固定波段，可以对任意频率进行调节，不仅适用于图示均衡器，也适用于参量均衡器。特别是采用快速傅里叶变换这样的算法，可以进行更快速的运算，即便是多段均衡器也不会引起运算量的增加。



Dynamic Range Control(DRC)动态范围控制提供压缩和放大能力，

可以使声音听起来更柔和或者更大声，即一种信号幅度调节方式。



Amlogic_DRC_Param_Generator

这个工具的用法

从名字上看，是drc参数生成器。

输入什么？输出什么？

```
-m：指定module名字。
	有4种情况：
	0：交叉filter。
	1：多个band的drc。
	2：全部band。
	3：clip 阈值。
-fc：指定中心频率。
-b：
	对于交叉filter的情况：0表示低通和中通，1表示中通和高通。
	对于多个band的drc：0/1/2依次表示低通、中通、高通。
	对于全部band的情况：0表示高的部分，1表示低的部分。
-a：attack时间，ms为单位。
-r：release时间。
-e：estimate时间。
-k：压缩率？
-t：阈值，最大是0DB
-o：用DB表示的偏移。-24dB到24dB。
-d：delay的sample个数。最大是255，大约5ms。
-D：dump寄存器。

```



```
Amlogic EQ param generator, version: 1.1 [Dec.24.2020]
Usage:  Amlogic_EQ_Param_Generator [-G] [-Q] [-fc] [-t] [-b] [-s] [-d]
    -G    logrithmic gain
    -Q    Q-term equating to (Fb/Fc)
    -fc   center frequency
    -t    filter type: 0: bandpass; 1: highpass; 2: lowpass;
    -b    band id, max 20 band (0~19)
    -D    dump all EQ registers
For example:
    [Set Parameters]
        Amlogic_EQ_Param_Generator -G 3.0 -Q 1.0 -fc 1000 -t 0 -b 0
    [Get Registers]
        Amlogic_EQ_Param_Generator -D
```



EQ/DRC module是amlogic 芯片中内置的一个硬件模块。

它是高速低功耗的音频后处理模块，用于音频的喇叭纠正和保护。





参考资料

1、

https://e2echina.ti.com/question_answer/analog/audio/f/42/t/15059

2、

https://www.cnblogs.com/yuanqiangfei/p/9896855.html