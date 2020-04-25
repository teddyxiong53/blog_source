---
title: esp8266之和nodemcu关系
date: 2018-11-29 21:00:35
tags:
	- esp8266

---



wemos、nodemcu、esp8266，这3者是什么关系？

nodemcu是以esp8266为基础做的开发板。

nodemcu = esp8266模组 + usb转串口芯片 + nodemcu firmware。

nodemcu还做到了对arduino的兼容。



我现在手里的这块就是nodemcu v3版本，使用的usb转串口芯片是CH340 。

NodeMCU is implemented in C and is layered on the Espressif NON-OS SDK.

nodemcu使用esp8266的 nonos版本的sdk作为基础，加入了lua解释器。



# 参考资料

1、

https://www.jianshu.com/p/cf5bd5820a08