---
title: Android系统之音频框架
date: 2020-06-24 15:13:51
tags:
	- Android

---

1

音频逻辑上相对比较简单，我以音频为切入点，来分析一下Android系统的整体框架。

在计算机发展的早起，电脑的声音处理设备就是一个简单的loudspeaker和Tone Generator构成。

功能非常有限。

后面人们想到以plugin的方式扩展音频设备。

这种早期的声卡以外接的方式插入主板上，这个就是独立声卡。

独立声卡的成本高。

所以后面又把声卡集成到主板上，就是集成声卡。

一个典型的声卡通常包括3个部分：

1、connectors。也叫jacks。就是跟耳机线的插口。

2、声卡主电路。

3、跟cpu的接口。例如PCI。

在我的手机上：

```
judyln:/ # cat /proc/asound/cards
 0 [sdm845tavilsndc]: sdm845-tavil-sn - sdm845-tavil-snd-card
                      sdm845-tavil-snd-card
```

市场的声卡非常多，对于一个os来说，应该怎样管理各种声卡，对上层提供统一的接口呢？

在Android系统里，很不是的tiny-xxx的项目。

因为完整的开源项目都比较大，所以就进行瘦身，就有了这些tiny项目了。

对于音频，是tinyalsa。在external目录下。

tinyalsa只支持了两种interface，而对于rawmidi、sequencer、timer都不支持。

对于嵌入式设备来说，够用了。

![1592984365434](../images/random_name/1592984365434.png)

Framework这一层，大家首先想到的是MediaPlayer和MediaRecorder。

因为这2个类，是我们在开发音频产品的时候，最常使用的类。

Android其实还提供了另外2个类似的类，AudioTrack和AudioRecorder。

但是没有前面那2个类简单易用。

另外还有：AudioManager、AudioService、AudioSystem这3个管理类。

Library这一层，在frameworks/av/media/libmedia目录下。用C++写的。

除了上面的这些代码，音频系统还需要一个中控。

在Android里，就是一个service。

对应的类是AudioFlinger、AudioPolicyService。

代码在frameworks/av/service/audioflinger。



分析这些类，可以有两条思路：

1、以库为主线。

2、以进程为主线。

比如AudioFlinger和AudioPolicyService都驻留于名为mediaserver的系统进程中;而AudioTrack/AudioRecorder和MediaPlayer/MediaRecorder一样实际上只是应用进程的一部分，它们通过binder服务来与其它系统进程通信。





参考资料

1、Android音频系统之音频框架

这篇文章条理清晰，非常好。

https://blog.csdn.net/dahailinan/article/details/24294655