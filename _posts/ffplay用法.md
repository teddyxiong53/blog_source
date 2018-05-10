---
title: ffplay用法
date: 2018-05-09 10:08:46
tags:
	- 视频

---



ffplay作为一个简单的播放器，可以在开发测试中发挥很大的作用。

1、播放本地h264文件。

```
ffplay -stats -f h264 test.264
```

2、点播rtsp。

```
ffplay rtsp://192.168.190.137/1.h264
```

