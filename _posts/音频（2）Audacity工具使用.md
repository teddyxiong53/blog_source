---
title: 音频（2）Audacity工具使用
date: 2018-05-31 21:52:09
tags:
	- 音频

---



这个工具当然不是最好的，但是是简单的，而且是开源的。

太专业的，东西太多，容易让我找不到北。



# 工具简介

audacity的字面含义是大胆、无耻的意思。（这个也是醉了，哈哈）。

audacity是一款免费的音频处理软件。最开始是在linux下发展起来的。使用gpl协议开源。

后面跨平台了。

可以用来录音和编辑音频。



# 简单使用

我们先在windows下载安装使用看看。

https://pc.qq.com/detail/0/detail_640.html

安装包10几M，安装后50M。不大。

启动后，有弹出帮助信息，我们可以快速看看。

我当前版本是2.2.2版本。

我随便找了一个安卓下的alarm.mp3文件。

长度是1分2秒。比特率是128kbps。大小是973KB。

但是我试图播放这个文件的时候，audacity总是提示

```
audacity 打开声音设备出错
```

我查看帮助里，诊断，音频设备信息，看到录音和播放的都是-1。

因为我开始打开软件的时候，没有插入耳机线。

我把软件退出，再重新打开，就可以看到诊断信息是这样的了。

```
==============================
Default recording device number: 1
Default playback device number: 3
==============================
Device ID: 0
Device name: Microsoft 声音映射器 - Input
Host name: MME
Recording channels: 2
Playback channels: 0
Low Recording Latency: 0.090000
Low Playback Latency: 0.090000
High Recording Latency: 0.180000
High Playback Latency: 0.180000
Supported Rates:
==============================
Device ID: 1
Device name: 麦克风 (2- USB2.0 MIC)
Host name: MME
Recording channels: 2
Playback channels: 0
Low Recording Latency: 0.090000
Low Playback Latency: 0.090000
High Recording Latency: 0.180000
High Playback Latency: 0.180000
Supported Rates:
==============================
Device ID: 2
Device name: Microsoft 声音映射器 - Output
Host name: MME
Recording channels: 0
Playback channels: 2
Low Recording Latency: 0.090000
Low Playback Latency: 0.090000
High Recording Latency: 0.180000
High Playback Latency: 0.180000
Supported Rates:
    8000
    9600
    11025
    12000
    15000
    16000
    22050
    24000
    32000
    44100
    48000
    88200
    96000
    176400
    192000
    352800
    384000
==============================
Device ID: 3
Device name: 扬声器 (Realtek High Definition
Host name: MME
Recording channels: 0
Playback channels: 2
Low Recording Latency: 0.090000
Low Playback Latency: 0.090000
High Recording Latency: 0.180000
High Playback Latency: 0.180000
Supported Rates:
    8000
    9600
    11025
    12000
    15000
    16000
    22050
    24000
    32000
    44100
    48000
    88200
    96000
    176400
    192000
    352800
    384000
==============================
Device ID: 4
Device name: 主声音捕获驱动程序
Host name: Windows DirectSound
Recording channels: 2
Playback channels: 0
Low Recording Latency: 0.120000
Low Playback Latency: 0.000000
High Recording Latency: 0.240000
High Playback Latency: 0.000000
Supported Rates:
==============================
Device ID: 5
Device name: 麦克风 (2- USB2.0 MIC)
Host name: Windows DirectSound
Recording channels: 2
Playback channels: 0
Low Recording Latency: 0.120000
Low Playback Latency: 0.000000
High Recording Latency: 0.240000
High Playback Latency: 0.000000
Supported Rates:
==============================
Device ID: 6
Device name: 主声音驱动程序
Host name: Windows DirectSound
Recording channels: 0
Playback channels: 2
Low Recording Latency: 0.000000
Low Playback Latency: 0.120000
High Recording Latency: 0.000000
High Playback Latency: 0.240000
Supported Rates:
    8000
    9600
    11025
    12000
    15000
    16000
    22050
    24000
    32000
    44100
    48000
    88200
    96000
    176400
    192000
==============================
Device ID: 7
Device name: 扬声器 (Realtek High Definition Audio)
Host name: Windows DirectSound
Recording channels: 0
Playback channels: 2
Low Recording Latency: 0.000000
Low Playback Latency: 0.120000
High Recording Latency: 0.000000
High Playback Latency: 0.240000
Supported Rates:
    8000
    9600
    11025
    12000
    15000
    16000
    22050
    24000
    32000
    44100
    48000
    88200
    96000
    176400
    192000
==============================
Device ID: 8
Device name: 扬声器 (Realtek High Definition Audio)
Host name: Windows WASAPI
Recording channels: 0
Playback channels: 2
Low Recording Latency: 0.000000
Low Playback Latency: 0.003000
High Recording Latency: 0.000000
High Playback Latency: 0.010000
Supported Rates:
    48000
==============================
Device ID: 9
Device name: 扬声器 (Realtek High Definition Audio) (loopback)
Host name: Windows WASAPI
Recording channels: 2
Playback channels: 0
Low Recording Latency: 0.003000
Low Playback Latency: 0.000000
High Recording Latency: 0.010000
High Playback Latency: 0.000000
Supported Rates:
==============================
Device ID: 10
Device name: 麦克风 (2- USB2.0 MIC)
Host name: Windows WASAPI
Recording channels: 1
Playback channels: 0
Low Recording Latency: 0.003000
Low Playback Latency: 0.000000
High Recording Latency: 0.010000
High Playback Latency: 0.000000
Supported Rates:
==============================
Selected recording device: 10 - 麦克风 (2- USB2.0 MIC)
Selected playback device: 3 - 扬声器 (Realtek High Definition
Supported Rates:

```

这一堆的信息，也不知道各个设备之间的关系和区别是什么。

然后可以进行录音。我是插着一个usb摄像头的。



# 简单应用





##把声音放大，缩小

操作之前，可以ctrl+A把音频进行选中，不选中是不能进行下面的操作的。

依次点击：效果，增幅（放大），在弹出窗口里进行拖拽操作即可。

## 截取一段

需要在时间轴哪里，右键菜单，选择启用拖拽选区。

然后鼠标点击一下，拖动一个范围，

然后文件，导出，导出选择的音频。

这样就可以把选择的部分导出成一个文件了。

## 分割立体声为单声道

在打开的音频的左上角那个音轨的下拉三角形那里，点击分割立体声到单声道。

然后就会出现2个音轨了。

然后我们可以把其中一个保存成文件就好了。

##降噪

我们先随便录一段，可以感觉明显的噪音。现在看看怎么降噪。

选择噪音部分的，选择效果，降噪。

的确效果很明显。







# 参考资料

1、百度百科

https://baike.baidu.com/item/audacity/585645?fr=aladdin

2、audacity使用教程

https://jingyan.baidu.com/album/25648fc18f24b29191fd0017.html?picindex=1

3、Audacity 音频编辑器教程

http://teliute.org/linux/Teauda/index.html