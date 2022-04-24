---
title: 音频alsa之drain和drop
date: 2022-04-15 16:35:11
tags:
	- 音频

---

--

可以看出，
snd_pcm_drain：对于播放，会先等待所有挂起没有传输完的数据帧先播完，才会去关闭PCM。
snd_pcm_drop：对于播放，会立即停止PCM，剩余的数据帧则直接丢弃不要。

从单词含义上就可以说明问题。

drain：耗尽。就是把没有传递完的数据传递完。

drop：丢弃。直接把剩下的数据丢掉。



参考资料

1、

https://blog.csdn.net/Guet_Kite/article/details/114383941