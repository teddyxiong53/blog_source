---
title: dlna之upmpdcli文档梳理
date: 2020-04-28 17:23:08
tags:
	- dlna

---

1

upmpdcli的官网文档对upnp描述很全面，所以我就索性把这个文档学习一遍。

# 介绍

upmpdcli是一个upnp renderer 前端，后端对接mpd。

它有很多的额外功能。

下一个小节解释了network audio相关术语。

upnp没有任何的安全规定。upmpdcli也没有专注安全性，所以有不少的安全问题。需要留意。

# upnp相关概念

## upnp av

upnp是一组网络协议。设计用来连接家庭网络里的设备。

upnp这个名字，就是因为这套方案，几乎不需要什么配置，就可以相互协调工作。

upnp的audio/video部分，简称为upnp av。实现了家庭网络里，音视频数据存放在一台设备上，而从另外一台设备进行播放的功能。

在一个network audio方案里，有4个组成部分：

```
1、音频数据存储设备。
	数据可以通过nfs、samba、http等方式进行访问。
2、directory/tag管理器。
	作用是用来从存储设备里抽象出一下标签来代表文件。
	构造一个数据库来管理访问。
3、audio player。也叫renderer。
	这个就是解码和发出声音的设备。
4、用户界面。
	用来控制音乐的播放。
```

在upnp的实现里，

```
tag manager被叫做MediaServer。
音频数据一般也是放在MediaServer里，但是也可以放在其他的机器上。
数据访问一般是通过http。

播放器叫做MediaRenderer。
用户界面叫做ControlPoint。
```

所以这里有个关键点：

playlist，是在ControlPoint里，而不是在renderer里。

renderer不会自动播放下一首。

多个ControlPoint共享一个renderer，就会导致混乱。

所以需要OpenHome这个东西。

# OpenHome

OpenHome是一组协议，设计的目的就是用来解决上面提到的upnp av的问题的。

原则上，OpenHome的playlist是在renderer上的。

在ControlPoint进入sleep状态后，renderer可以自己继续播放。

这是一个很大的优点，很多的ControlPoint，例如Android下的BubbleUPnP就支持OpenHome。

除了playlist，OpenHome还支持一些其他的功能。

例如，访问Internet radio。

audio data的地址，在OpenHome里叫做source。

例如：radio source，playlist source。

任何支持OpenHome的ControlPoint，都可以进行source的切换操作。

一个source，由一个type和一个name来唯一标定。

# songcast

songcast是一个协议，用来做实时network audio的传输的 。

它跟upnp唯一的关系是，upnp服务控制了连接。

songcast运行在多个player上播放相同的音频。而且可以保证几乎完全同步。

或者实时采集音频并进行播放。

所以songcast包括2个部分：

1、sender。

2、receiver。

# gapless

这个是一个相对较小的功能点。

但是大家都此都很敏感。



# upmpdcli概览

upmpdcli支持gapless track transition。

支持OpenHome服务。

还实现了songcast协议。让音箱端可以作为一个songcast的sender或者receiver。

提供了一个MediaServer接口。当前是用来访问外部的流服务，例如spotify。

可以被安装在大多数的Linux系统上。在树莓派上用得很多。

很多的针对音频领域的Linux发行版本，把upmpdcli作为默认的upnp Media Renderer。

在很多商业设备上也有用。



大部分的配置通过配置文件来设置，有些也可以通过环境变量或者命令行参数来设置。

配置文件格式就是key-value对。

配置文件内容较多，但是是分section的。

还有一个图形界面的工具可以帮助你进行配置。



# upmpdcli Media Renderer

本节讨论renderer的其他方面的细节。

默认upnp av和OpenHome接口都是打开的。

只有OpenHome的ControlPoint可以共享同一个设备。

upnp av如果多个ControlPoint控制同一个设备，则会导致混乱。



# 音频格式

upmpdcli支持的音频格式，就是mpd支持的音频格式，这几乎包括了所有的格式。

upmpdcli会先检查一下，但是这个检查行为可以用参数关闭。

mpd处理有些通过http传输的格式，有些问题。

wav文件和aiff文件，尤其是格式多于16bit的。这个问题很多。

具体的表现，取决于mpd的版本和插件（可以是ffmpeg、libaudiofile、libsndfile）。

经常有这种情况，文件本地播放是好的，但是通过http播放就不行。

raw pcm是另外一个特别情况。原因是pcm里不带音频的属性信息。



参考资料

1、官网文档

https://www.lesbonscomptes.com/upmpdcli/upmpdcli-manual.html

2、OpenHome就是这个公司设计的协议。songcast也是。

https://www.linn.co.uk/