---
title: alsa之Master音量
date: 2022-05-10 16:33:01
tags:

	- alsa

---

--

我看电脑，还是某些板子上，都有一个Master Volume来控制音量。

但是我调的板子都没有。

今天才弄清楚，因为我的板子都是多个codec芯片。

例如2片tas5707 ，在设备树里，就需要配置prefix，不然会初始化失败。

如果只有一片tas5707，则不需要prefixname。这样就可以看到Master Volume。



