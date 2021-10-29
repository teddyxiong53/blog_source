---
title: 音频之opus编码
date: 2018-12-22 17:21:17
tags:
	- 音频
---





opus是一种音频编码格式。使用场景是网络上的实时音频传输。

完全开放的，没有专利限制。



pcm编码为opus。怎么做？



opus集成了两种声音编码技术：

1、以语音编码为导向的silk。语音。

2、低延迟的celt。音乐。

opus可以无缝调节高低比特率。

opus有非常低的算法延迟，默认为22.5ms。最低为5ms。

非常适合用于语音对讲。

**比mp3、aac这些，有更低的延迟。**

mp3的延迟比较大，不适合流媒体。



https://opus-codec.org/

从官网下载libopus。运行里面的opus_demo。

基本用法：

```
./opus_demo [-e] <application> <sample_rate> <channels> <bits per second> <input> <output>
```

-e：表示只使用encoder。

Application：voip、audio、restricted-lowdelay这三种情况。

举例：

```
./opus_demo -e voip 16000 1 16000 1.pcm 2.opus
```

得到的opus文件，没法直接播放。因为并没有封装ogg文件头。

但是可以在转码成pcm来播放。

```
./opus_demo -d  16000 1  2.opus 3.pcm
```

3.pcm可以正常播放。



智能硬件中经常会遇到语音链路解决方案，例如：人机对话、口语评测等。

为了提高智能终端的交互成功率，推荐在硬件本地进行音频压缩，以降低对于网络带宽等环境的要求。

在考虑到方案的通用性基础上，往往会支持多种音频编码方式，像是speex、amr等，但是依旧推荐用户优先使用opus。

既然是面向B端的解决方案，那么最初就要考虑是否具备通用性。

Opus的免费开源，且功能强大，基本上在方案的推广上，各大芯片商和硬件方案商对该格式的支持也是较为普遍。

整体方案适合实时语音传输，同时方便文件存储

在传输过程中，Opus官方推荐使用RTP包头进行封装便于语音传输，同时以OGG形式进行存储。

Opus的编码规则使得编码和拼接变得非常方便，在云端音频处理的过程中带来了极大的便利度。



在保存环节，可以将opus转为ogg格式进行存储，该格式本身支持opus编码，因此该转换并不需要重新编解码，而只需要用过ogg文件格式重新进行封装即可，目前各大音频播放器对ogg的解码支持也很通用。



目前我经常使用到语音技术有语音识别和口语评测，讯飞、阿里云、捷通华声、先声等语音开放平台对Opus均有良好的支持，只是各家服务供应商对于Opus的包头均进行了二次封装。



由于目前普遍使用RTP包头进行Opus编码的封装，

该包头包含8个字节，

可是对于16k采样率单声道人声场景，

其实包头中只有包身长度为有效数据（一个字节足矣）。

站在通信的效率上，各家对包头进行重新封装，

有包头仅保留一个字节标记长度，

也有使用两个字节标记长度（大小端存储方式也需要被考虑），

此时为了保证整体服务对于供应商不要产生强依赖，

建议在云端进行兼容，即让所有用户均以标准的8字节RTP包头进行请求，

而云端进行二次封装，由于该封装不涉及编解码，

仅需要删除掉不需要的字节，因此处理效率还是比较高的。



# 参考资料

1、opus

https://baike.baidu.com/item/opus/680370?fr=aladdin

2、opus维基百科

https://zh.wikipedia.org/wiki/Opus_(音频格式)

3、Opus: 音频编码器的瑞士军刀

https://zhuanlan.zhihu.com/p/24883553

4、opus格式真的比aac要好吗？

https://www.zhihu.com/question/55194135

5、Opus Recommended Settings

https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&mobileaction=toggle_view_desktop

6、人声应用场景的王者——Opus

https://zhuanlan.zhihu.com/p/309381487

7、编解码器杂谈：浅析 Opus

https://zhuanlan.zhihu.com/p/66719842