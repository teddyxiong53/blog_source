---
title: 网络电台icecast了解
date: 2020-03-03 17:17:28
tags:
	- 音视频

---

1

icecast 是一个流媒体服务器，支持ogg、opus、web、MP3这些码流。

可以用来创建一个网络电台，或者一个私人点唱机。

使用GPLv2开源的。

最近的发布版本是2.4.3，是2019年1月发布的。

编译：

```
   ./configure
   make
   make install
```

configure报错。

```
configure: error: XSLT configuration could not be found
```

安装软件：

```
sudo apt-get install libxslt-dev
```

还是报错

```
error: must have Ogg Vorbis v1.0 or above installed
```

```
sudo apt-get install libogg-dev libvorbis-dev
```



怎样运行？

每个server可以做多个广播。也就是支持多个流媒体。

一个收听者，只能收听其中的一个。

默认的安装路径是/usr/local/share/icecast。

这个下面有3个目录：web、doc、admin。

doc下面是放配置文件的。把icecast_minimal.xml.dist这个拷贝，改名为：icecast.xml

里面需要修改的。host要改一下。改成你的ip地址就好了。

```
icecast -c /usr/local/share/icecast/doc/icecast.xml
```

然后放一个UrlPlayer.mp3文件到web目录下。

客户端，用浏览器进行测试。

路径类似这样：

```
http://172.16.4.205:8000/UrlPlayer.mp3
```

 Ices2是一个将音频数据发送到Icecast2服务器以广播给客户端的程序。 Ices2可以从磁盘（Ogg Vorbis文件）中读取音频数据，也可以从声卡中采集现场音频，并对其进行编码。 在本文中，我们将让Ices2从本地硬盘读取.ogg文件。

Ices2仅支持Ogg Vorbis文件，因此如果您要流式传输的.mp3文件，则应将其转换为.ogg。



ices2的代码在这里，github上没有代码。

https://salsa.debian.org/multimedia-team/ices2



```
sudo apt-get install libshout3-dev
```

默认的安装目录是/usr/local/share/ices。

使用方法：

```
ices config.xml
```

我看看/usr/local/share/ices/ices-alsa.xml这个文件。

可以跑起来。

默认是实例文件是example1.ogg。

所以我用浏览器访问地址：

```
http://172.16.4.205:8000/example1.ogg
```




# ices2代码分析

用ldd /usr/bin/ices2，看到依赖的动态库还是不少。

```
libasound.so
libvorbisenc.so
libvorbis.so
libshout.so
libxml2.so
libogg.so
libcrypto.so
libspeex.so
...
```

依赖xml库，是因为配置文件是用xml写的。

配置文件有4个例子。

```
alsa
oss
playlist
roar
```

roar这个是什么场景呢？

roar的字面意思是咆哮。

doc目录下有文档。

## basic

```
it's purpose is to stream whatever it is given into a stream for feeding to the Icecast streaming server. 
```

ices2的目的是把收到的数据，转成stream，发送给icecast服务器。

```
RoarAudio driver and libs available at The RoarAudio site
```

从这里看，roar代表的是一个音频库，RoarAudio。这个库的特点是什么？



RoarAudio的网站在这里：http://bts.keep-cool.org/

RoarAudio是一个现代声音系统，特点是强大的协议。

硬件和系统无关。

完全网络透明。

RoarAudio是以协议为核心的。

我不管。

就用alsa的就好了。



ices2可以同时发给多个icecast服务器。

在发送之前，会进行预处理，例如重采样、或者downmixing（把双声道变成单声道），用来适应网络带宽。



因为ices2的代码并不多，逻辑也不复杂，所以doc下面的文档完全是够用了。讲得也非常清楚了。

## config

一个xml配置文件的总体布局是：

```
 <?xml version="1.0"?>
 <ices>
 	general settings//通用配置
 	stream section//stream配置。
 </ices>
```

### 通用配置部分

```
是否后台运行
日志文件路径
日志文件名字
日志文件大小限制
日志级别
是否在控制台打印
pid文件路径
```

### Stream配置部分

```
元数据metadata
输入input
实例instance
```

#### 元数据包括

```
name
genre 体裁，就是音乐风格，例如Rock
描述
url：网站的地址。
```

这部分没有什么实际作用，只是用来显示的。

#### 输入

从alsa或者playlist进行输入。

```
<input>
	<module>alsa</module>
	<param name="rate">44100</param>
	//其他的param
</input>
```

#### 实例

```
<instance>
	<hostname>
	<port>
	<password>
	<mount>
	<yp>//是否在网络上发布你的服务。默认否。不用打开这个。
	<encode>
		<quality>
		<samplerate>
		<channels>
	<downmix>
	<resample>
		<in-rate>44100
		<out-rate>22050
	<savefile>
</instance>

```

yp server是什么？

yp是Yellow Page（黄页）的意思。

也叫Network Information Service，NIS。



# libshout

看到依赖了libshout这个库，这个库的作用是什么？

http://icecast.org/news/libshout-release-2_4_2/

只有一个头文件：shout.h。

注释里写着：

```
API for libshout, the streaming library for icecast
```

这个库就是icecast的一部分。

接口不多，就10几个函数。

代码在这里。

https://github.com/xiph/Icecast-libshout

从ices2的代码看，libshout是负责把编码后的ogg数据发送到icecast服务器上。

所以涉及http通信这些。



参考资料

1、官网

http://icecast.org/

2、Manuais/Icecast

http://w.hacklaviva.net/articles/m/a/n/Manuais_Icecast_1d66.html

3、运行自己的Webradio站与Icecast2和Ices2

https://www.howtoing.com/linux_webradio_with_icecast2_ices2