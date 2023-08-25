---
title: 音频之amixer命令
date: 2019-05-16 15:15:11
tags:
	- 音频

---

--

# alsa的命令分类

alsa的命令有3套。

```
这个是alsa官方的。
aplay
arecord
amixer

这个是图形界面的。调试用。
alsaconf
alsactl    
alsamixer  
alsaucm

这个是Android里的tiny版本。
tinycap
tinyplay
tinymix
```

主要以alsa官方的为主。



命令的基本格式：

```
amixer [options] [cmd]
```

选项：

```
-c, --card N
	指定声卡
-D, --device N
	选择设备，默认是default设备。
-d, --debug
	debug模式。
-n, --nocheck
	不要进行range检查。
-v, --version
	版本。
-q, --quiet
	不要打印。
-i, --inactive
	把不活跃的也显示出来。
-a, --abstract L
	选择抽象级别。none或者basic
-s, --stdin
	从stdin连续得到输入命令。
-R, --raw-volume
	使用raw value。默认就是的。
-M, --mapped-volume
	使用映射过的volume值。
	
```

命令：

```
scontrols
	显示所有的mixer简单控制项。
scontents
	显示mixer contents
sset id value
	作用类似tinymix set id value
sget id
controls
contents
cget id value
	c表示one control。
cget id
```

调节音量：

amixer set Master 100%



Mic Boost

run amixer to select the correct input source and type:



amixer info

```
teddy@thinkpad:~$ amixer info
Card default 'Intel'/'HDA Intel at 0xf2600000 irq 27'
  Mixer name    : 'Realtek ALC269'
  Components    : 'HDA:10ec0269,17aa212a,00100004'
  Controls      : 23
  Simple ctrls  : 11
```

amixer scontrols

```
teddy@thinkpad:~$ amixer scontrols
Simple mixer control 'Master',0
Simple mixer control 'Headphone',0
Simple mixer control 'Speaker',0
Simple mixer control 'PCM',0
Simple mixer control 'Mic',0
Simple mixer control 'Mic Boost',0
Simple mixer control 'Beep',0
Simple mixer control 'Capture',0
Simple mixer control 'Auto-Mute Mode',0
Simple mixer control 'Digital',0
Simple mixer control 'Loopback Mixing',0
```



# 一些例子

## 1

```
amixer -c 1 sset Line,0 80%,40% unmute cap
```

这个的作用是设置第二个声卡的left line input音量为80%，right line input为40% 。

并且解除禁麦，而且设置为录音接口。

这个是官方的例子，对于我的笔记本，应该是：

```
amixer -c 0 sset Mic,0 80%,40% unmute cap
```

可以正常设置：

```
teddy@thinkpad:~$ amixer -c 0 sset Mic,0 80%,40% unmute cap
Simple mixer control 'Mic',0
  Capabilities: pvolume pswitch
  Playback channels: Front Left - Front Right
  Limits: Playback 0 - 31
  Mono:
  Front Left: Playback 25 [81%] [3.00dB] [on]
  Front Right: Playback 13 [42%] [-15.00dB] [on]
```

## 2

```
amixer -c 0 -- sset Master playback -20dB
```

```
teddy@thinkpad:~$ amixer -c 0 -- sset Master playback -20dB
Simple mixer control 'Master',0
  Capabilities: pvolume pvolume-joined pswitch pswitch-joined
  Playback channels: Mono
  Limits: Playback 0 - 64
  Mono: Playback 44 [69%] [-20.00dB] [on]
```

注意sset前面那2个`-`是不能省略的。

如果Master有多个声道，那个多个声道都设置为相同的值。



## 3

```
amixer -c 0 set PCM 2dB+
```

把声卡0的音量提高2dB，包括录音和播放的。



怎样理解录音的volume？





Mic Boost是什么？

# amixer cget和sget区别是什么

在 ALSA（Advanced Linux Sound Architecture）中，`amixer` 是一个用于控制和调整音频设置的命令行工具。在使用 `amixer` 命令时，你会经常看到 `cget` 和 `sget` 这两个选项，它们在功能和用法上有一些区别。

1. **`cget`（Capture Get）：** `cget` 选项用于获取捕获（录制）音频设置的当前值。它可以用于查询当前音频输入设备（如麦克风）的设置参数，如音量、增益等。

   例如，使用以下命令可以获取当前捕获音频设备的音量设置：

   ```bash
   amixer cget numid=1
   ```

   在输出中，你将看到当前音量设置的详细信息。

2. **`sget`（Switch Get）：** `sget` 选项用于获取开关类型设置的当前状态。它通常用于查询音频设备上的开关设置，比如静音状态。

   例如，使用以下命令可以获取音频设备的静音状态：

   ```bash
   amixer sget Master
   ```

   在输出中，你将看到当前静音状态的详细信息。

总之，`cget` 用于获取捕获（录制）音频设置的当前值，而 `sget` 用于获取开关类型设置的当前状态。它们是 `amixer` 命令的不同选项，用于查询和显示音频设置的信息。

# 参考资料

1、linux 用命令设置系统音量大小

https://blog.csdn.net/matthew0618band/article/details/17224983

2、man手册

这里给了几个例子。

https://linux.die.net/man/1/amixer