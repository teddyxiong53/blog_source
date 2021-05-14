---
title: 音频之pcm-mmap
date: 2021-05-11 13:38:34
tags:
	- 音频
---

--

要使用mmap，首先需要把access type改成SND_PCM_ACCESS_MMAP_INTERLEAVED

而不是用SND_PCM_ACCESS_RW_INTERLEAVED



参考资料

1、AAudio 和 MMAP

https://source.android.com/devices/audio/aaudio?hl=zh-cn