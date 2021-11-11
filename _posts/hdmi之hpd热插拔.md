---
title: hdmi之hpd热插拔
date: 2021-11-10 15:49:43
tags:
	- hdmi

---

--

HDMI (Pin 19)/DVI（Pin16）的功能是热插拔检测（HPD），

这个信号将作为HDMI 源端（Source）是否发起EDID读，是否开始发送TMDS信号的依据。

HPD是从HDMI显示器端（Sink）生成

并输出送往HDMI 源端（Source）的一个检测信号。

热插拔检测的作用是当显示器等HDMI接口的显示设备通过HDMI/DVI接口与HDMI 源端（Source）相连或断开连接时，

HDMI源端（Source）能够通过HDMI/DVI的HPD引脚检测出这一事件，并做出响应。

下面以HDMI为例讲述HPD的原理和实现方式。



参考资料

1、HDMI接口之HPD（热拔插）

https://blog.csdn.net/jiayu5100687/article/details/81604739

