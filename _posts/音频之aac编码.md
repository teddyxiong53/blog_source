---
title: 音频之aac编码
date: 2020-02-19 14:11:51
tags:
	- 音频

---

1

什么是aac编码？跟mp3编码的关系是什么？哪个更好？适用的场景是什么？

出现于1997年， 基于 MPEG-2的音频编码技术。

由Fraunhofer IIS、杜比实验室、AT&T、Sony（索尼）等公司共同开发，**目的是取代MP3格式。**

2000年，**MPEG-4标准 出现后，AAC 重新集成了其特性，加入了SBR技术和PS技术**，为了区别于传统的 MPEG-2 AAC 又称为 MPEG-4 AAC。

编解码的最大的使用场景，其实不是电脑上存储音频文件的格式。

因为现在电脑硬盘很便宜，即使你保存原始音频文件，都没有什么压力。

而是在广播电视传输上。这个带宽一定是受限的。



其实已经很流行，只不过不是在纯音频领域，比如目前优酷等视频网站的flv格式中，对音频的封装都是用AAC，毕竟在视频厂商来看，AAC比MP3节省的那点点流量是非常有意义的，省流量就是省钱，积少成多。

AAC格式的主要扩展名有三种：

AAC - 使用MPEG-2 Audio Transport Stream( ADTS，参见MPEG-2 )容器，**区别于使用MPEG-4容器的MP4/M4A格式**

M4A - 为了区别纯音频MP4文件和包含视频的MP4文件而由苹果(Apple)公司使用的扩展名，Apple iTunes 对纯音频MP4文件采用了".M4A"命名。M4A的本质和音频MP4相同，故音频MP4文件亦可直接更改扩展名为M4A。

作为一种高压缩比的音频压缩算法，AAC压缩比通常为18：1，也有资料说为20：1，远胜mp3



# adts

在调试ffmpeg的例子transcode_aac的是，发现adts这个东西。



MP3的一帧数据是1152个采样点的数据。44.1K的采样率的话。

那么一帧的数据，就就是23ms左右的。

而aac的一帧数据是1024个采样点。44.1K的采样率的话。一帧的时长也是23ms左右。

用1024主要是因为AAC是用的1024点的mdct。





swr_convert的第三个参数，不能传输出的frame_size。

因为mp3转aac，1152-》1024,采样数会溢出，导致fifo并不是满的。数据会丢。

所以换成了传input frame的nb_samples，这样，不论是1152-》1024还是1024-》1152,都可以保证数据不会丢失。

通道数和channel layout的对应关系。

```
    { "mono",        1,  AV_CH_LAYOUT_MONO },
    { "stereo",      2,  AV_CH_LAYOUT_STEREO },
```



adts的header是7个字节。

```
#define AV_AAC_ADTS_HEADER_SIZE 7
```



参考资料

1、AAC 音频流的封装

https://meta.appinn.net/t/aac/10963

2、既然 AAC 要比 MP3 好，且体积差不多，为什么网上不流行 AAC 格式的音频呢？

https://www.zhihu.com/question/20756052

3、AAC ADTS格式分析

https://blog.csdn.net/tantion/article/details/82743942

4、音频帧frame的长度

http://blog.sina.com.cn/s/blog_8af106960102y7dz.html

5、编解码学习笔记（五）：Mpeg系列——AAC音频

https://blog.csdn.net/flowingflying/article/details/5718594?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task