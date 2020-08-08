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
./opus_demo -e voip 16000 1 16000 1.pcm 1.opus
```

这里写opus文件的时候。



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