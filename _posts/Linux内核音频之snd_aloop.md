---
title: Linux内核音频之snd_aloop
date: 2021-10-28 14:59:25
tags:
	- Linux内核

---

--

用aplay -l查看，看看有没有loopback的设备，

如果没有，使用modprobe snd-aloop来进行插入。



使用ALSA Loopback方式内录音频，可以录取声卡输出的音频而不影响正在播放的音频。

播放音频
aplay -fS16_LE -r16000 xxxx.pcm

录取输出音频
arecord -fS16_LE -r16000 -D "hw:Loopback,1,0" -c2 xxxx.pcm



参考资料

1、Linux上用ALSA aloop driver实现录制其他程序播放的声音

https://blog.csdn.net/lsheevyfg/article/details/116799564

