---
title: 智能音箱之vad
date: 2020-08-10 16:10:47
tags:
	- 音箱

---

1

现在需要做本地vad。所以研究一下这个主题。

这个有个例子。在我的笔记本跑一下看看。

https://github.com/Baidu-AIP/speech-vad-demo

这个也是一个例子。但是代码看起来比较多。

https://github.com/dpirch/libfvad



unimrcp中vad算法的诸多弊端，但是有没有一种更好的算法来取代呢。

目前有两种方式 1. GMM   2. DNN。

 其中鼎鼎大名的WebRTC VAD就是采用了GMM 算法来完成voice active dector。

今天笔者重点介绍WebRTC VAD算法。

下面的章节中，将介绍WebRTC的检测原理。



首先呢，我们要了解一下人声和乐器的频谱范围，下图是音频的频谱。

根据音频的频谱划分了6个子带，

80Hz~250Hz，

250Hz~500Hz,

500Hz~1K,

1K~2K,

2K~3K,

3K~4K，

分别计算出每个子带的特征。

WebRTC的检测模式分为了4种:

 0:  Normal, 1. low Bitrate   2.Aggressive  3. Very Aggressive ，其激进程序与数值大小相关，可以根据实际的使用在初始化的时候可以配置。

vad 支持三种帧长，80/10ms   160/20ms   240/30ms 

采样这三种帧长，是由语音信号的特点决定的，**语音信号是短时平稳信号，**

在10ms-30ms之间被看成平稳信号，高斯马尔可夫等**比较信号处理方法基于的前提是信号是平稳的。**



 WebRTC 支持8kHz 16kHz 32kHz 48kHz的音频，但是WebRTC首先都将16kHz 32kHz 48kHz首先降频到8kHz，再进行处理。

参考资料

1、第七章 语音检测(VAD)原理和实例

https://shichaog1.gitbooks.io/hand-book-of-speech-enhancement-and-recognition/content/chapter7.html

2、

https://www.cnblogs.com/damizhou/p/11318668.html