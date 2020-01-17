---
title: 音频之multiroom
date: 2019-12-25 16:17:51
tags:
	- 音频

---

1

直接在搜索引擎查找，感觉找不到什么东西。

在github里搜索“multiroom”。

用谷歌搜索“multiroom audio open source”。

https://github.com/strobe-audio/strobe-hub

这个不行，还很初期。

树莓派和snapcast结合

就是hass里集成。



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



编译运行看看。

必须以git clone的方式进行下载，因为还有子模块需要clone。

为了加快速度，从gitee进行下载。

```
https://gitee.com/max-liulin/snapcast.git
```

然后下载子模块。这些就只能从github这些地方下载了。比较慢。

```
git submodule update --init --recursive
```

挂着梯子下载会快点。

我采用笔记本跟Android手机连在同一个路由器下面。这种方式来进行测试。

apk文件从这里下载：

https://github.com/badaix/snapdroid/releases/tag/v0.17.1.1

笔记本上编译好。笔记本作为server，也做一个client。另外手机做另外一个client。

笔记本上开3个shell窗口：

第一个窗口，运行server：

```
./snapserver 
```

第二个窗口，运行client：

```
./snapclient -h 172.16.4.205
```

第三个窗口，使用ffmpeg给/tmp/snapinfo提供数据：

```
ffmpeg -y -i /home/teddy/work/dossos/test/resource/UrlPlayer.mp3 -f u16le -acodec pcm_s16le -ac 2 -ar 48000 /tmp/snapfifo
```

server运行的打印：

```
teddy@teddy-ThinkPad-SL410:~/work/snapcast/snapcast/server$ ./snapserver 
2020-01-15 18-04-22 [Notice] Settings file: "/home/teddy/.config/snapserver/server.json"
2020-01-15 18-04-22 [Info] Adding service 'Snapcast'
2020-01-15 18-04-22 [Info] PcmStream sampleFormat: 48000:16:2
2020-01-15 18-04-22 [Info] metadata={
2020-01-15 18-04-22 [Info]     "STREAM": "default"
2020-01-15 18-04-22 [Info] }
2020-01-15 18-04-22 [Info] onMetaChanged (default)
```

因为我的笔记本上有两个网卡，一个有线，一个无线，有线的是接入都另外的一个网络了。

所以希望server可以运行在无线网卡上，但是实际上是运行在有线网卡上。

从上面的打印看，生成了一个配置文件server.json。

```
2020-01-15 18-04-22 [Notice] Settings file: "/home/teddy/.config/snapserver/server.json"
```

打开这个文件，把里面的网卡相关信息都改成无线网卡的。

重新启动server。

手机上打开app，添加笔记本的ip地址，然后就可以了。

可以实现笔记本和手机同步播放同一个音乐。



参考资料

1、在Volumio整合SnapCast有最好的多房间系统

http://www.bujarra.com/integrando-snapcast-en-volumio-para-tener-el-mejor-sistema-multiroom/?lang=zh

2、树莓派 HiFi DAC 扩展板 Volumio 安装使用教程

http://shumeipai.nxez.com/hifidac-hat-for-raspberry-pi-volumio-instructions