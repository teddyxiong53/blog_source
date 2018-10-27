---
title: gstreamer用法
date: 2018-04-30 09:14:53
tags:
	- video

---



# gstreamer是什么

gstreamer是一个框架，用来构建流媒体应用。是一个非常强大和通用的框架。

它的优点主要来自于的它的模块性。

目的是简化音视频应用开发的难度。

基本设计思想来自于俄勒冈研究生学院有关视频管道的创意。同时也借鉴了DirectShow的设计思想。

在编写同时有视频和音频的应用程序时，gstreamer可以让你的工作变得简单。

gstreamer的应用不限于媒体流。可以处理任意的数据流。

gstreamer的主要用途就是做播放器。

插件和管道，是gstreamer最主要的设计思想。

0.9版本之后的插件，名字上被分为了3类：

1、good。

2、bad。

3、ugly。



# 基本使用

一个简单的mp3播放器的例子，放在这里。



# 基础概念

##GstAppSrc



## GstElement



# 参考资料

1、百科。

https://baike.baidu.com/item/gstreamer/10998598?fr=aladdin

2、中文手册

https://wenku.baidu.com/view/95f916c708a1284ac850432a.html

3、gstreamer，vlc，ffmpeg比较

https://blog.csdn.net/ds1130071727/article/details/78492566?locationNum=9&fps=1

4、gstreamer插件指南

https://blog.csdn.net/sinat_28502203/article/details/46010485