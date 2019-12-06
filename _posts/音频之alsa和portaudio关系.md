---
title: 音频之alsa和portaudio关系
date: 2019-05-28 17:37:51
tags:
	- 音频

---

1

Linux音频的问题就是太复杂了。

音频处理本质上比其他处理要复杂。

```
alsa
portaudio
gstreamer

```

portaudio是对alsa这些进行了再一次的封装，使用上更加简单了。

portaudio是跨平台的库。



参考资料

1、Linux 音频系统简析

http://www.embeddedlinux.org.cn/html/xinshourumen/201008/31-849.html