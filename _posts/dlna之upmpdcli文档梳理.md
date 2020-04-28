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





参考资料

1、官网文档

https://www.lesbonscomptes.com/upmpdcli/upmpdcli-manual.html

2、OpenHome就是这个公司设计的协议。songcast也是。

https://www.linn.co.uk/