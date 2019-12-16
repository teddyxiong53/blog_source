---
title: Linux内核之音频子系统
date: 2019-12-13 16:18:25
tags:
	- Linux内核

---

1

目前Linux中主流的音频体系结构是alsa。

alsa在驱动层提供了alsa-driver，在应用层提供了alsa-lib。

在Android里，没有使用标准的alsa，而是使用了简化版本的tinyalsa。但是在内核中仍然使用ALSA框架的驱动框架。

Android中使用tinyalsa控制管理所有模式的音频通路。





参考资料

1、linux驱动由浅入深系列：tinyalsa(tinymix/tinycap/tinyplay/tinypcminfo)音频子系统之一

https://blog.csdn.net/radianceblau/article/details/64125411