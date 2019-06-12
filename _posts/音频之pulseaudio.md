---
title: 音频之pulseaudio
date: 2019-06-11 15:56:51
tags:
	- 音频

---

1

看设备信息，看到PulseAudio Sound Server。这个究竟是什么？

```
teddy@teddy-ThinkPad-SL410:~$ aplay -L
null
    Discard all samples (playback) or generate zero samples (capture)
pulse
    PulseAudio Sound Server
default
    Playback/recording through the PulseAudio sound server
```

是基于posix接口的声音系统。为Linux开发，可以移植到支持posix的os上。

是一个守护进程，接收其他进程的数据，转发给硬件。

类似的有：

1、alsa是mixer。

2、jack。



参考资料

1、What Is PulseAudio?

https://www.freedesktop.org/wiki/Software/PulseAudio/

2、

https://baike.baidu.com/item/PulseAudio/22718056?fr=aladdin