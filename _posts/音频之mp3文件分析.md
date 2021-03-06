---
title: 音频之mp3文件分析
date: 2019-06-04 15:53:51
tags:
	- 音频

---

1

MP3是利用人耳对高频声音信号不敏感的特性，

**将时域波形信号转换成频域信号，**

**并划分成多个频段，**

**对不同的频段使用不同的压缩率，**

对高频加大压缩比（甚至忽略信号）对低频信号使用小压缩比，保证信号不失真。

这样一来就相当于**抛弃人耳基本听不到的高频声音，**

只保留能听到的低频部分，从而将声音用1∶10甚至1∶12的压缩率压缩。

由于这种压缩方式的全称叫MPEG Audio Player3，所以人们把它简称为MP3。

最高参数的MP3(320Kbps)的音质较之CD的,FLAC和APE无损压缩格式的差别不多，其优点是压缩后占用空间小，适用于移动设备的存储和使用。



mp3全称是MPEG Audio Layer 3。

是一种高效的音频编码方案。

还有mp1、mp2这2种方案。

```
MP3全称是MPEG1 Audio layer 3。
MPEG是运动图片专家组的缩写。
音频相关的标准有：
	MPEG-1
	MPEG-2
		MPGE-1和MPEG-2使用同一组音频编码解码族：layer1、layer2、layer3
		1、2、3这些数字，是根据压缩质量和编码复杂程度来命名的。
		分别对应mp1、mp2、mp3这3种文件。MP3的压缩率最高，也最复杂。
		采样率一般为：32K、44.1K、48K。
		我们重点看layer3，前面两种不怎么用的。
		mp3的设计码率在128kbps左右。压缩比在10:1左右。
		常用的编码器是LAME，它完全遵循LGPL的MP3编码器，有着良好的速度和音质。
	MPEG-2 AAC
	MPEG-4
```



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



比如常见mp3为[MPEG-1](https://www.baidu.com/s?wd=MPEG-1&tn=SE_PcZhidaonwhc_ngpagmjz&rsv_dl=gh_pc_zhidao) Layer III，而这个规格的采样个数固定为1152（下面公式已经化简过了）。



这个是mp3解码库。

https://github.com/lieff/minimp3



**时域和频域是信号的基本性质**，这样可以**用多种方式来分析信号**，每种方式提供了不同的角度。

解决问题的最快方式不一定是最明显的方式，**用来分析信号的不同角度称为域**。时域频域可清楚反应信号与互连线之间的相互影响。





https://github.com/toots/shine

https://github.com/cpuimage/tinymp3





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

7、mp3

https://baike.baidu.com/item/mp3/23904

8、时域频域

https://baike.baidu.com/item/%E6%97%B6%E5%9F%9F%E9%A2%91%E5%9F%9F/9399325#2

9、MP3 编码解码 附完整c代码

https://www.cnblogs.com/cpuimage/p/9427457.html