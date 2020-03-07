---
title: nmap命令
date: 2020-03-04 09:33:28
tags:
	- 

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



参考资料

1、官网

http://icecast.org/

2、Manuais/Icecast

http://w.hacklaviva.net/articles/m/a/n/Manuais_Icecast_1d66.html