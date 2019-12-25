---
title: 音频之multiroom
date: 2019-12-25 16:17:51
tags:
	- 音频

---

1

直接在搜索引擎查找，感觉找不到什么东西。

在github里搜索“multiroom”。



# snapcast

https://github.com/badaix/snapcast

Snapcast是多房间客户端服务器音频播放器，其中所有客户端都与服务器同步，以播放完全同步的音频。 

它不是一个独立的播放器，而是一个扩展，把你现有的音频播放器变成一个 sonos，像多个房间解决方案。 
服务器输入的音频是命名管道 /tmp/snapfifo。 
所有输入到这个文件的数据将被发送到已经连接的客户端。 
在使用Snapcast的最常用方法之一是与音乐播放器守护进程( MPD ) 或者 Mopidy 结合使用，
它可以配置为使用指定的管道作为音频输出。

通过与Snapclients的TCP连接发送编码块。 
每个客户端都与服务器进行持续时间同步，以便客户端总是知道本地服务器时间。 
每个接收到的块首先解码并添加到客户端的块缓冲区。 
了解服务器的时间，在适当的时候使用ALSA来播放块。 
时间偏差修正方式：
	跳过零件或者整个块
	播放静音
	播放速度更快/较慢
	通常偏差小于 1毫秒。



参考资料

1、在Volumio整合SnapCast有最好的多房间系统

http://www.bujarra.com/integrando-snapcast-en-volumio-para-tener-el-mejor-sistema-multiroom/?lang=zh

2、树莓派 HiFi DAC 扩展板 Volumio 安装使用教程

http://shumeipai.nxez.com/hifidac-hat-for-raspberry-pi-volumio-instructions