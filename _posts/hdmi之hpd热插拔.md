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



显示器通过HDMI连接HDMI源端设备，当HDMI 源端（Source）通过HDMI接口的HPD引脚检测到显示器与HDMI源端（Source）相连时（HPD从低电平到高电平），HDMI 源端（Source）认为已经有显示设备连接，并通过HDMI接口中的显示器数据通道DDC（DDC I2C总线）读取显示器EDID存储器中存储的EDID数据（扩展显示器识别数据），如果检测到显示器的工作模式范围与HDMI 源端（Source）的输出设置相适应，则HDMI 源端（Source）就激活TMDS信号发送电路发送正常的HDMI信号给显示设备。

所以Sink端的EDID是在HPD从低电平到高电平的转换时被HDMI Source端读取的。

**如果需要强制刷新EDID， 可以发起一个HPD信号（拉低HPD,再拉高HPD），让HDMI source来读取新的EDID内容。**



显示器断开HDMI连接时，当HDMI 源端（Source）通过HPD引脚检测到显示器的HDMI接口与HDMI 源端（Source）断开时，HDMI 源端（Source）就断开TMDS信号发送电路，停止发送HDMI信号。



HDMI 源端（Source）对HPD信号的要求，

```
大于2.4v，认为是连接的。
低于0.4v，认为是断开的。
```



**HPD信号的实现一般是在HDMI的Sink端，**

通过一个1K欧姆的电阻上拉到HDMI +5V，同时，本地的主处理器可以通过一个GPIO来控制它，如下图所示。



一个HDMI设备的EDID 通常包含两个模块，

第一个是EDID1.3的数据模块，

第二个是CEA 861B模块，

这个861B模块中，一定要包含数据标示符 0x000C03。

HDMI发送设备（Source）检测到HPD 信号由低变高时，就会去读取Sink端的EDID 数据，来确认接收装置是否出现变化，并确定是工作在HDMI模式还是DVI模式。



# 参考资料

1、HDMI接口之HPD（热拔插）

https://blog.csdn.net/jiayu5100687/article/details/81604739

2、

https://blog.csdn.net/zhiyuan2021/article/details/115211169