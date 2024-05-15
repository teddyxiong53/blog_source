---
title: dlna相关之AirPlay
date: 2020-04-28 15:17:08
tags:
	- dlna

---

1

代码：https://github.com/juhovh/shairplay

直接编译通过，在笔记本上进行测试。可以正常发现和使用。

没有明显异常。

比gmrender的表现要好不少。

# 简介

下表为您提供了关于AirPlay的简介：

| 名称     | AirPlay                                                      |
| -------- | ------------------------------------------------------------ |
| 定义     | AirPlay是由苹果公司开发的一种无线流媒体传输技术。            |
| 功能     | 允许用户从iOS设备、macOS设备或iTunes向支持AirPlay的设备传输音频、视频、照片和屏幕镜像。 |
| 设备支持 | AirPlay可以用于苹果设备（如iPhone、iPad、Mac）与支持AirPlay的音箱、电视、投影仪等设备之间的互联。 |
| 特点     | 实时性好、易于使用、高质量的音频和视频传输、支持多种媒体类型。 |

AirPlay通过Wi-Fi网络实现设备之间的连接和通信，用户可以通过简单的操作在不同设备之间共享媒体内容或屏幕。

# 发展历史

以下是AirPlay的主要发展历史：

| 日期   | 事件                                                         |
| ------ | ------------------------------------------------------------ |
| 2010年 | AirPlay首次在iOS 4.2系统中推出，最初称为AirTunes。用户可以使用它将音频从iOS设备流式传输到支持AirPlay的扬声器。 |
| 2011年 | 随着iOS 4.3的推出，AirPlay扩展到视频流，用户可以将视频从iOS设备或iTunes流式传输到支持AirPlay的电视。 |
| 2012年 | AirPlay Mirroring功能首次在iOS 5中推出，允许用户将iOS设备上的屏幕镜像到支持AirPlay的电视或投影仪上。 |
| 2013年 | iOS 7中引入了多房间音频功能，使用户可以在多个房间同时播放音频。 |
| 2015年 | AirPlay 2推出，是AirPlay的第二个主要版本，支持多房间音频同步播放和更强大的音频控制功能。 |
| 2018年 | AirPlay 2得到进一步改进，支持更多第三方设备和更多功能。      |

AirPlay从最初的音频流式传输功能逐步发展成为一个支持音频、视频和屏幕镜像的多媒体传输技术，并且逐步增强了对多房间音频同步播放和第三方设备的支持。

# 非苹果设备支持

虽然AirPlay最初是由苹果公司开发的，但是一些第三方设备也开始支持AirPlay。以下是一些主要的非苹果设备，它们支持AirPlay功能：

| 品牌     | 设备类型           | AirPlay支持情况                 |
| -------- | ------------------ | ------------------------------- |
| 蓝牙音箱 | 一些蓝牙音箱支持   | 通过AirPlay进行音频传输。       |
| 电视     | 部分智能电视支持   | 可以通过AirPlay进行视频传输。   |
| 扬声器   | 一些智能扬声器支持 | 支持通过AirPlay进行音频传输。   |
| 接收器   | 一些音频接收器支持 | 可以接收通过AirPlay传输的音频。 |

虽然非苹果设备对AirPlay的支持程度可能会有所不同，但它们可以允许用户通过AirPlay将音频或视频从iOS设备、macOS设备或iTunes传输到这些设备上。

# 开源实现

以下是一些开源实现AirPlay功能的项目：

| 项目名称       | 描述                                                         |
| -------------- | ------------------------------------------------------------ |
| ShairPort-sync | ShairPort-sync是一个基于开源项目ShairPort的分支，它允许Linux设备充当AirPlay接收器。 |
| RAOP-Player    | RAOP-Player是一个用Python编写的简单的AirPlay音频播放器，可以在Linux上运行。 |
| node-airtunes2 | node-airtunes2是一个使用Node.js实现的AirPlay音频流服务器，可以在Linux上运行。 |
| Airplay SDK    | Airplay SDK是一个多平台的开源AirPlay媒体流传输库，支持Linux、Windows和macOS等平台。 |

这些项目为开发者提供了在Linux平台上实现AirPlay功能的选项，可以用于将Linux设备转换为AirPlay接收器或媒体服务器。



# shairport-sync

https://github.com/mikebrady/shairport-sync

这个也是AirPlay的一个实现。在buildroot里自带了。

看最近的更新在2个月前，说明这个项目还算活跃。

而且，snapcast直接支持shairport-sync。那么毫无疑问，shairport-sync就是我想要的。

AirPlay具备与DLNA所没有的镜像功能，这一功能叫**AirPlay镜像**，可将iPhone 或iPad 上的画面无线传输到电视上，也就是说你设备显示的是什么，电视屏幕显示就就是什么，而不仅限于图片和视频。你可以拿着iPad 来当做方向盘，然后看着大屏玩游戏。

另外AirPlay镜像最牛地方是它可以实现双屏游戏，让你的游戏有更多的交互。比如，电视里显示的是游戏画面，而iPad上显示的是比赛的路线图。



DLNA是基于文件的，媒体文件可能有各种各样的编码格式，播放器这端必须能够处理这么多种编码格式。通常为了比较好的播放体验，DLNA会先缓存一小段时间。

Miracast是实时的，它可以实时传输源端(Source)的输出。源端任何屏幕的操作都会被传输到接收(Sink)端。如果源端是播放媒体文件，源端负责先对媒体文件解码，然后再编码成H.264的格式。接收端只需要做H.264的解码就可以了。相对DLNA，Miracast对于WiFi通路的要求要更高一些。



跟snapcast配合是这样的。

```
shairport-sync -o stdout > /tmp/snapfifo
```

虽然这样是可以工作的。但是我觉不应该是我手动来重定向。当前如果不重定向，就是直接把二进制数据输出到控制台了。

因为snapcast的文档里写了这样配置：

```
stream = airplay:///shairport-sync?name=Airplay
```

看snapcast的代码注释里这样写：

```
snapserver -s "airplay:///shairport-sync?name=Airplay
```

我上面重定向的方式，是不太对的。

应该这样执行shairplay-sync。

```
shairport-sync -o stdout -d
```

snapcast怎样支持多个输入呢？如何在多个输入之间切换呢？



我就这样处理，也没有问题：

1、snapserver.conf里，仍然只保留一个/tmp/snapfifo的。

2、这样启动shairplay-sync。

```
shairplay-sync -d -o stdout > /tmp/snapfifo
```

这样就都统一为snapfifo的方式了。



```
  config.udp_port_base = 6001;
  config.udp_port_range = 100;
  config.output_format = SPS_FORMAT_S16; // default
  config.output_rate = 44100;            // default
```

退出只能用：

```
shairplay-sync -k
```

看起来代码写得不太好。



**使用了rtsp来做媒体数据传输。**

**AirPlay是把解码后的数据发送过来播放。**



看看默认的配置文件shairplay-sync.conf

```
general
	name：默认是hostname（把首字母大写）
	output_backend = "alsa";
	mdns_backend = "avahi";
	port = 5000; 这个是rtsp监听的端口
    run_this_when_volume_is_set = "/full/path/to/application/and/args";
    	这个是一个hook。调节音量的时候，可以调用一个自己的程序。
    	
session control
	run_this_before_play_begins = "/full/path/to/application and args"
		也是一个hook。播放的时候调用。
	run_this_after_play_ends = "/full/path/to/application and args";
		一个hook，播放完成后调用。
		
backend setting
	alsa
	sndio
	pa
	pipe
		name = "/path/to/pipe";
	dsp
	metadata
```



```
avahi: service '25B3280FF49F@Rockchip' successfully added.

连接的时候：
New RTSP connection from 192.168.0.101:57800 to self at 192.168.0.102:5000 on conversation thread 0.
断开的时候：
RTSP conversation thread 0 terminated.
再次连接：
New RTSP connection from 192.168.0.101:57810 to self at 192.168.0.102:5000 on conversation thread 1.
```

点击播放时：

```
Output frame bytes is 4.
Output bit depth is 16.
Dithering will be enabled because the output volume is being altered in software
Set initial volume to -18.000000.
Using negotiated latency of 77175 frames and a static latency correction of 0
Hammerton Decoder used on encrypted audio.
Output written using MMAP
```

点击暂停几秒后：

```
Player thread exit on RTSP conversation thread 1.
RTSP conversation thread 1 terminated.
```

从端口情况看，在手机上暂停，跟选择本机播放是一样的，都是断开了跟音箱端的rtsp在5000端口的连接。

所以，AirPlay只能从手机这边发起控制，不能从板端控制手机的播放和暂停。



再看延时问题。

直接输出到alsa进行播放，这个看起来没有明显延迟。



# AirPlay协议

Bonjour是苹果为基于组播域名服务(multicast DNS)的开放性零设置网络标准所起的名字。使用Bonjour的设备在网络中自动传播它们自己的服务信息并聆听其它设备的服务信息，设备之间就象在打招呼，这也是命名为Bonjour(法语：你好)的原因。

将ios手机接入wifi后用wireshark抓包能够看到192.168.1.100 向 224.0.0.251 port 5353 发送广播.

操作手机，打开媒体播放器时，ios会用MDNS发送Queries，其中有两项服务`_raop._tcp.local`和`_airplay._tcp.local`，

Airplay用Bonjour做设备发现，在windows中安装BonjourSDKforWin,在任务管理器中有mDNSResponder.exe进程用于mdns协议处理。





# 参考资料

1、基于树莓派的AirPlay功能实现

https://blog.csdn.net/hhyqhh/article/details/76692010

2、

https://blog.csdn.net/bxjie/article/details/39581565

3、AirPlay非官方协议文档

http://nto.github.io/AirPlay.html

4、AirPlay2技术浅析

https://www.pianshen.com/article/8543281968/