---
title: 智能音箱之Jasper
date: 2019-06-20 17:10:37
tags:
	- 音频
---

1

Linux音频层次结构

```
app
--------------
应用框架：portaudio、pyaudio、gstreamer
-----------------
音频服务器：pulseaudio、jackd
----------------
驱动：alsa、oss
---------------
内核
```

Jasper的音频输入：用pyaudio。

音频输出：espeak。aplay。pymad。这3种。

espeak语音合成。aplay播放离线提示音。pymad播放url。



参考资料

1、Jasper语音助理

https://www.cnblogs.com/hzl6255/p/8215551.html#AudioSystem

2、

https://post.smzdm.com/p/595414/