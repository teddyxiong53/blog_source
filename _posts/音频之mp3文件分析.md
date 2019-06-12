---
title: 音频之mp3文件分析
date: 2019-06-04 15:53:51
tags:
	- 音频

---

1

mp3全称是MPEG Audio Layer 3。

是一种高效的音频编码方案。

还有mp1、mp2这2种方案。

MPEG标准，跟音频相关的有：

MPGE-1/MPEG-2/MPEG2-AAC/MPEG-4。

mp3用的是MPEG-1的。

mp3采用了感知音频编码这种有损编码方式。

去掉了大量的冗余信号和无关信号。

mp3文件由多个帧组成。

帧是mp3文件的最小组成单位。

每帧包括：

1、帧头。记录了码率、采样率、crc、

2、附加数据。

3、声音数据。

每帧的播放时长是0.026秒。

mp3文件的组成

```
1、ID3V2。可以没有。
	位于文件首部。长度不固定。包含作者等信息。
	是对ID3V1的扩展。
	组成：
		1、一个标签头。
			10个字节。
		2、若干个标签帧。
			每个标签帧都有10字节的帧头。
2、音频帧数据。
	帧头是4个字节。
	组成：
		1、帧头。4字节。必须有。
		2、CRC。2字节，可以没有。
		3、通道信息。32字节。必须有。
		4、声音数据。长度不固定。必须有。
3、ID3V1
```

ID3V2有4个版本：

2.1

2.2

2.3：最流行的是这个版本。

2.4

mp3 每帧均为1152个字节， 则：

frame_duration = 1152 * 1000000 / sample_rate

例如：sample_rate = 44100HZ时， 计算出的时长为26.122ms，这就是经常听到的mp3每帧播放时间固定为26ms的由来。



找一些mp3分析工具。

https://en.softonic.com/download/mp3-frame-editor/windows/post-download

看看这个怎么样。

不行，不支持mpeg2 。



一帧的采样个数是576个。就是1152字节。

这个是对于MPEG2、level3的。是这个数。

我用百度语音合成的16k采样率的文件，看帧头是：

```
FFF3 28C4
```

每一帧是68字节。

这个68是怎么来的？是1152字节压缩得到的吗？





这个是mp3解码库。

https://github.com/lieff/minimp3



参考资料

1、

https://blog.csdn.net/qingkongyeyue/article/details/70984891

2、MP3文件结构解析(超详细)

https://blog.csdn.net/u010650845/article/details/53520426

3、计算音频帧的播放时间(音频码流 音频帧)

https://blog.csdn.net/weiyuefei/article/details/74333499

4、

https://www.jianshu.com/p/c3f8be205e3f

5、Mp3帧分析（数据帧）

https://blog.csdn.net/qq_24004499/article/details/79584495

6、

https://blog.csdn.net/zhenglie110/article/details/78654410