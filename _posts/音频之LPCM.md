---
title: 音频之LPCM
date: 2021-11-10 14:25:43
tags:
	- 音频

---

--

多声道LPCM：

无损音轨原始存在格式，

概念上等效于wave文件，

并不需要运算解码，

可直接输入功放进行DA转换，

**光纤和同轴接口只能传输2声道LPCM，**

**多声道LPCM需要HDMI接口传输。**

PCM:非线性脉冲编码调制
LPCM:线性脉冲编码调制



PCM中有时会使用相应的技术降低数字信号源的数据率,便于存储和数据传输方便

LPCM中通常使用了更多的杜比环绕立体声重放技术,更逼真地再现原声场。

LPCM(PCM)（线性脉冲编码调制）



转换流程:抽样 --> 量化 --> 编码
\-------------------------------------------------------------
抽样过程是将连续时间模拟信号变为离散时间,连续幅度的抽样信号

量化过程是将抽样信号变为离散时间,离散幅度的数字信号

量化过程又被分为：

1、线性量化

2、非线性量化

线性量化在整个量化范围内,**量化间隔均相等**

非线性量化采用不等的量化间隔



主要区别:

因为它们量化间隔不同,所以最后的二进制编码位数不同.

其它区别:

PCM中有时会使用相应的技术降低数字信号源的数据率,便于存储和数据传输方便

LPCM中通常使用了更多的杜比环绕立体声重放技术,更逼真地再现原声场。



LPCM(PCM)（线性脉冲编码调制）　　

普通CD规格为16bit/44.1kHz，

DVD的规格则有多种，量化精度可分为16bit、20bit、24bit，

采样频率分为48kHz、96kHz。



此外,LPCM[信号](http://baike.baidu.com/view/54338.htm)中可录入杜比[环绕声](http://baike.baidu.com/view/853256.htm)信息，供现有的[杜比定向逻辑](http://baike.baidu.com/view/495130.htm)环绕声系统使用。



VOB文件有[视频](http://baike.baidu.com/view/16215.htm)、声音、字幕数据流组成。

```
VOB是DVD光盘里直接拷贝出来的文件，你可以直接拖入播放器播放，但是这样将无法看到内含的字幕，且一个VOB文件只是电影的一部分。
```



视频数据流是MPEG2格式，

[音频](http://baike.baidu.com/view/66105.htm)数据流是AC-3或者者LPCM、MPEG2、MP2、DTS等等，

AC3基本上是事实的标准，

MPEG2多声道只在极少数2区碟上可以看到(比如In the line of fire，2区).

PCM主要用于音乐DVD，

而MP2只在廉价DVD上才有.

PCM是高质量无压缩数字音频，因此需要太多的空间，并不适合用于DVD电影光碟。

AC3的数据率介于`192~448KBPS之间，192KBPS用于双声道，384~448KBPS`用于[5.1声道](http://baike.baidu.com/view/190268.htm)。



音频数字化主要有压缩与非压缩两种方式。

较早出现的数字音频播放机，如CD唱机和DAT[录音机](http://baike.baidu.com/view/29010.htm)，均采用线性PCM[编码](http://baike.baidu.com/view/237708.htm)来存储音乐信号，为非压缩方式。

在高质量要求的音频工作站和数字录像机（如DVCPRO）上，现在也采用非压缩的格式。



我们目前常见的MPEG、Dolby Digital、DTS等则为压缩方式。

压缩分为有损压缩和无损压缩。

有损压缩的目的是提高[压缩率](http://baike.baidu.com/view/354638.htm)，降低占用[系统资源](http://baike.baidu.com/view/53557.htm)。

可以根据实际需要选用不同的采样速率、样本分辨力（精度）和数据率。



如今[杜比数字](http://baike.baidu.com/view/53407.htm)作为由FCC为[美国](http://baike.baidu.com/view/2398.htm)选定的ATSC数字电视标准的一部分，

为[高清晰度电视](http://baike.baidu.com/view/70858.htm)（HDTV)和标准清晰度电视（SDTV)广播的标准。

MPEG为[欧洲](http://baike.baidu.com/view/3622.htm)数字视频广播（DVB)、数字音频广播（DAB）和[日本](http://baike.baidu.com/view/1554.htm)广播电视业的音频标准。



DVD则支持3种主要标准：

Dolby digital（杜比数字）、

[MPEG-2](http://baike.baidu.com/view/7747.htm)

线性PCM(LPCM)。



其他格式，如DTS(Digital Theatre Sound)、SDDS(Sony Dynamic Digital Sound)等为任选格式。



声音重放技术的发展路程，

是沿着[单声](http://baike.baidu.com/view/67727.htm)(Monophonic)、双[声道](http://baike.baidu.com/view/117427.htm)立体声(Stereophonic)到4通道立体声，

再到环绕立体声(Stereo surround)，

现在一般为5.1模式。



其根本目的，就是更逼真地再现原声场。



我国电视目前大量采用的单声道已远远跟不上人们生活的需要。



如何以最低的数据率，最有效地传送多声道、高质量的声音，是数字化的发展方向。

所谓5.1模式，即录制、解码和放声中采用5个声道：

左（L）、中（C）、右(R)、左环绕（LS)、右环绕RS)，

再加上一个低频效果通道(LFE)，



就可以达到真正的立体环绕声效果——宽阔的场景深度感和总体真实感。



5.1模式为ATSC和DVB的标准声道。



声音之所以能够数字化，是因为人耳所能听到的声音频率不是无限宽的，主要在20kHz以下。



按照抽样定理，只有抽样频率大于40kHz，才能无失真地重建原始声音。

**如CD采用44.1kHz的抽样频率，其他则主要采用48kHz或96kHz。**





有时候PCM和LPCM都被笼统地统称为PCM，但是他们不完全一致。





eARC 接口支持8 通道192 kHz *PCM* 音频和高比特率音频(*HBR*) 压缩音频格式



# 参考资料

1、音频输出PCM与LPCM有什么不同

https://www.cnblogs.com/lihaiping/p/lpcm.html

2、LPCM

https://baike.baidu.com/item/LPCM/13347759

3、

https://zh.wikipedia.org/zh-tw/%E7%B7%A8%E8%A7%A3%E7%A2%BC%E5%99%A8%E5%88%97%E8%A1%A8