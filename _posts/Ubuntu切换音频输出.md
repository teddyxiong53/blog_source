---
title: Ubuntu切换音频输出
date: 2021-04-29 10:49:34
tags:
	- Ubuntu
---

--

现在有个需求，要在命令行切换音频的输出方式。

切换到hdmi、蓝牙、耳机这3个。

这个命令列出所有的输出设备。

```
pacmd list-cards | grep output\:
```

pacmd - Reconfigure a PulseAudio sound server during runtime

**This command is what worked for me:**

```
pactl set-card-profile 0 output:hdmi-stereo
```

This is how I switched back to my laptop's internal speakers:

```
pactl set-card-profile 0 output:analog-stereo
```

我感觉pactl set-default-sink SINK这个命令是我想要的。

当前`pactl list sinks`，只能看到一个，

```
amlogic@amlogic-BAD-INDEX:~$ pactl list sinks
Sink #0
        State: SUSPENDED
        Name: alsa_output.pci-0000_00_1f.3.analog-stereo
        Description: Built-in Audio Analog Stereo
        Driver: module-alsa-card.c
        Sample Specification: s16le 2ch 48000Hz
        Channel Map: front-left,front-right
        Owner Module: 7
```

我连上hdmi的设备，看这个还是只有一个，那么就不是这么弄的。

是因为电脑只要一个声卡。

这个可以切到hdmi。

```
pactl set-card-profile 0 output:hdmi-stereo
```





参考资料

1、

https://askubuntu.com/questions/539768/how-can-i-change-audio-output-to-hdmi-from-command-line