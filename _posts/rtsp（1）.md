---
title: rtsp（1）
date: 2018-04-29 21:27:46
tags:
	- rtsp

---



#流媒体定义

流媒体有广义和狭义的两种定义。

广义上是指，使得音频和视频形成稳定、连续的传输流和回放流的一系列技术、方法、协议的总和。

狭义上是指，相当于传统的下载播放方式而言，支持多媒体数据的实时传输和实时播放。



#流媒体协议

1、实时传输协议。RTP。

可以单播，也可以多播。

一般是基于UDP的。

RTP协议包括：RTP数据协议和RTP控制协议。

RTSP位于RTP和RTCP之上。目的是通过IP网络有效地传输多媒体数据。

## RTSP/RTP/RTCP关系

一句话概括，就是RTSP用来start、stop传输，RTP用来传输媒体数据，RTCP对RTP进行控制、同步。

RTSP里的setup方法，就确定了RTP/RTCP的端口。

RTSP里的play、pause、teardown，就控制了RTP的状态。

RTCP包括Sender Report和Receiver Report。用来进行音视频的同步。

## RTP协议

先看头部的构成。

对应的文档是RFC3550 。RFC1889是老版本。

在RFC3550里，不仅定义了RTP，还定义了配套的RTCP协议。

RTP不保证服务质量，由PTCP来保证。











# 参考资料

1、RTP协议学习大总结从原理到代码

https://wenku.baidu.com/view/aaad3d136edb6f1aff001fa5.html?sxts=1525008415053

2、RTP/RTSP/RTCP有什么区别？

https://www.zhihu.com/question/20278635