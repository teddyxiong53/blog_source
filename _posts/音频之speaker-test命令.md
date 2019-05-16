---
title: 音频之speaker-test命令
date: 2019-05-16 15:38:11
tags:
	- 音频
---





这个也是alsa utils的一个。

基本格式：

```
speaker-test [options] ...
```

选项：

```
-D, --device
	指定设备。
-r, --rate
	指定频率，单位hz。
-c, --channels
	指定通道数。
-f, --frequency
	指定频率。
-F, --format
	指定格式。
-b, --buffer
	us为单位。ring buffer的大小。
-p, --period
	us为单位。period的单位。
-P, --nperiods
	周期数。
-t, --test
	可以是sine和pink、wav。
-l, --nloops
	指定测试周期。0表示无限。
-s, --speaker
	单喇叭测试。1表示left，2表示right。
-w, --wavfile
	在-t后面是wav时，要加上这个参数来指定播放哪个wav文件。
-W, --wavdir
	指向一个包含wav文件的目录。
-m, --chmap
	指定通道映射。
-S, --scale
	指定百分比，默认80。
	
```

