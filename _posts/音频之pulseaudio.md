---
title: 音频之pulseaudio
date: 2019-06-11 15:56:51
tags:
	- 音频

---

--

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



==简单说，pulseaudio是为了解决alsa存在的混音能力不足而出现的。==

整体解决方案是：

==pulseaudio作为一个守护进程，独占声卡。==

其他程序要发声，就发消息给pulseaudio进程。

==在Android里，使用了AudioFlinger来替代pulseaudio的功能。==

启动：

```
pulseaudio --system --daemonize
```



相关的配置文件在/etc/pulse目录下。

```
teddy@teddy-ThinkPad-SL410:/etc/pulse$ ls
client.conf  daemon.conf  default.pa  system.pa
```



相关命令：

```
paplay
pacmd
```



# 参考资料

1、What Is PulseAudio?

https://www.freedesktop.org/wiki/Software/PulseAudio/

2、

https://baike.baidu.com/item/PulseAudio/22718056?fr=aladdin

3、Linux Audio Stack & ALSA

https://blog.csdn.net/cnclenovo/article/details/47106743