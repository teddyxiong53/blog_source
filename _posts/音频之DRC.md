---
title: 音频之DRC
date: 2020-04-06 10:10:51
tags:
	- 音频

---

1

DRC，全称是Dynamic Range Compress。动态范围压缩。

主要的作用是限制喇叭的功率输出。

简单的讲，DRC可以帮助我们设定比较大的增益放大小信号，大信号时又不失真。

不失真的提升平均音量，此功能还可以保护喇叭。

如果没有DRC，音量控制相对比较尴尬，音量过大会使大信号音源经放大后失真；音量过小会导致小信号音源的时候整体输出音量不够。

rk3308的方案里，有一个eq_drc_process进程。

启动脚本是这样：

```
aplay -D softvol /oem/silence.wav
/oem/acodec-gain.sh &
export EQ_LOW_POWERMODE=true
export PLAYBACK_HPF_PASS=0hz
case "$1" in
	start)
		# ueventd
		cp -rf /etc/presetFile.sat /data/presetFile.sat
		sleep 1
		/usr/bin/eq_drc_process &
		;;
```



acodec-gain.sh 这个脚本的内容：

这个没有什么内容，就是用amixer设置一下Master的音量。



参考资料

1、

https://e2echina.ti.com/question_answer/analog/audio/f/42/t/15059