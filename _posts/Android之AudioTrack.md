---
title: Android之AudioTrack
date: 2018-05-27 18:18:53
tags:
	- Android

---



对于Android开发人员来说，最熟悉的音频回放类是MediaPlayer。

而AudioTrack则用得比较少。

因为MediaPlayer是封装了AudioTrack，用起来更加简单。



AudioTrack用于pcm音频流的回放。在数据传送上有两种方式：

1、调用write方法，把音频数据push到AudioTrack里去。

2、数据接收方主动去pull。



传送数据，有两种模式。

1、static模式。数据一次性送过去。适合铃声这种数据量小的情况。

2、streaming模式。



# 参考资料

1、Android音频系统之AudioTrack(一)

https://blog.csdn.net/edmond999/article/details/18600323