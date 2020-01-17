---
title: homeassistant之多房间音乐播放集成
date: 2020-01-16 13:51:19
tags:
	- homeassistant
---

1

需要的组件有：

mopidy

snapcast

# mopidy

官网：https://mopidy.com/

介绍写着：

```
mopidy是一个可扩展的music server，用python写的。
可以播放这些地方的音乐：本地音乐、Spotify、SoundCloud、Google Play Music等。
你可以在手机上编辑播放列表。
```

对云音乐的播放支持是靠插件来完成的。

没有安装插件的mopidy只能播放本地文件和radio stream。

mopidy是一个http server，通过安装mopidy-mpd插件，可以同时成为一个mpd-server。

官方github：https://github.com/mopidy

```
sudo pip3 install Mopidy
```

运行一下：

```
mopidy --help
```

出错了。

```
ValueError: Namespace Gst not available
```

那这个是依赖了gstreamer了。

安装gstreamer。

```
sudo apt-get install gstreamer-1.0
```

也报错了。

```
The following packages have unmet dependencies:
 gstreamer1.0-omx-dbg : Depends: gstreamer1.0-omx (= 1.0.0.1-0+rpi12+jessiepmg) but 1.14.4-1+rpt1 is to be installed
 gstreamer1.0-python3-dbg-plugin-loader : Conflicts: gstreamer1.0-python3-plugin-loader but 1.14.4-1 is to be installed
 gstreamer1.0-python3-plugin-loader : Conflicts: gstreamer1.0-python3-dbg-plugin-loader but 1.14.4-1 is to be installed
E: Unable to correct problems, you have held broken packages.
```

暂时不在树莓派上做了。

在我的笔记本上进行测试。

查看mopidy的依赖：

```
teddy@teddy-ThinkPad-SL410:~/work$ mopidy deps
Executable: /usr/bin/mopidy
Platform: Linux-4.4.0-171-generic-i686-with-Ubuntu-16.04-xenial
Python: CPython 2.7.12 from /usr/lib/python2.7
Mopidy: 2.0.0 from /usr/lib/python2.7/dist-packages
GStreamer: 1.8.3.0 from /usr/lib/python2.7/dist-packages/gi
  Detailed information: 
    Python wrapper: python-gi 3.20.0
    Relevant elements:
      Found:
        uridecodebin
        souphttpsrc
        appsrc
        alsasink
        osssink
        oss4sink
        pulsesink
        flump3dec
        id3demux
        id3v2mux
        lamemp3enc
        mad
        mpegaudioparse
        mpg123audiodec
        vorbisdec
        vorbisenc
        vorbisparse
        oggdemux
        oggmux
        oggparse
        flacdec
        flacparse
        shout2send
      Not found:
        none
```

直接执行mopidy看看。

有打印错误：

```
ERROR    Frontend (MpdFrontend) initialization error: MPD server startup failed: [Errno 98] Address already in use
INFO     HTTP server running at [::ffff:127.0.0.1]:6680
INFO     Starting GLib mainloop
```

搜索一下，看看是哪个进程占用了对应的端口：

```
teddy@teddy-ThinkPad-SL410:~$ sudo netstat -nlp |grep 6600
tcp6       0      0 :::6600                 :::*                    LISTEN      1/init  
```

为什么是init进程呢？

所以需要先研究一下mpd的用法。



# snapcast

仓库里默认就所有snapcast的。

```
pi@raspberrypi:~ $ sudo apt-cache search snapcast
snapclient - Snapcast client
snapserver - Snapcast server
```

树莓派上就安装snapserver的。

hass官网上说，snapcast的版本要高于0.5.0的。

安装的版本足够新。

```
pi@raspberrypi:~ $ snapserver --version
snapserver v0.15.0
```



参考资料

1、

https://www.home-assistant.io/blog/2016/02/18/multi-room-audio-with-snapcast/