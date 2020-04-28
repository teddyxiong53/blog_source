---
title: dlna之协议分析
date: 2020-04-28 13:44:08
tags:
	- dlna

---

1

# dlna、miracast、AirPlay对比

这3种协议，都是实现了类似的无线播放功能。

它们之间具体有什么区别？

dlna特别一些，因为它实际上是推送了一个连接过来，还是要播放设备值去链接指向的位置去获取音视频数据。

而miracast和AirPlay，跟蓝牙类似，音视频数据是手机解码后发送过来的。



miracast是WiFi联盟在2012年指定的。以wifi直连为基础的无线投屏协议。

miracast有跟AirPlay类似的镜像功能。就是把手机屏幕内容直接投屏到电视上。

Android4.2以后标配了这个功能。

画面延迟在150ms以内。



dlna的是以upnp协议为基础，专注于流媒体设备的设备控制与播放。

但是音频和视频的体验都不是很好，**音视频体验不及airplay和mircast**。

这套协议的初衷是能让各种设备互联，通用性足够了，但是各家的细节各有不同，导致体验上不来。

**airplay虽然设备局限性大，但是稳定性足够。**而且随着手机越来越大，用户于更趋向于直接看手机或电视，手机推送的场景已经越来越少了。

由于技术的局限和使用场景的局限性，用户始终没培养起来使用这项技术的习惯。



参考资料

1、

https://www.bijienetworks.com/news/airplay-vs-miracast-vs-dlna/

2、

https://www.zhihu.com/question/56054162