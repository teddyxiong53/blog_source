---
title: 音频之alsabat
date: 2021-05-27 13:47:11
tags:
	- 音频

---

--

bat是Basic Audio Tester的缩写。

自动测试audio driver和sound server。

不需要人工交互。

bat通过自播自录，然后分析录到的音频。

BAT supports ALSA/tinyalsa/PulseAudio/Cras backend. 

由3部分组成：

playback, capture and analysis.

BAT supports 5 working modes:

 loopback, 

single line playback, 

single line capture, 

local 

standalone mode.



参考资料

1、bat

https://www.alsa-project.org/main/index.php/BAT