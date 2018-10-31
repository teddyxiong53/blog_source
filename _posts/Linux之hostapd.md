---
title: Linux之hostapd
date: 2018-10-30 13:19:14
tags:
	- Linux

---



简单来说，hostapd就是用来把无线网卡模拟成一个ap热点的工具。

模拟的ap称为Soft AP。

hostapd就是作为softap的认证服务。

负责接入设备的认证。

怎样查看一款无线网卡是否支持ap模式呢？

用iw工具。

```
iwlist
```

```
# iwlist
Usage: iwlist [interface] scanning [essid NNN] [last]
              [interface] frequency 
              [interface] channel 
              [interface] bitrate 
              [interface] rate 
              [interface] encryption 
              [interface] keys 
              [interface] power 
              [interface] txpower 
              [interface] retry 
              [interface] ap 
              [interface] accesspoints 
              [interface] peers 
              [interface] event 
              [interface] auth 
              [interface] wpakeys 
              [interface] genie 
              [interface] modulation 
```





# 参考资料

1、Linux下软AP功能之Hostapd介绍

https://blog.csdn.net/hinyunsin/article/details/6029663

2、（一）hostapd是干嘛的

https://www.kancloud.cn/digest/wlan/141028