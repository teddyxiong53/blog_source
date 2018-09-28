---
title: 树莓派之搭建echo
date: 2018-05-09 10:35:01
tags:
	- 树莓派

---



#在亚马逊上注册你的设备。

得到一个client id和一个client secret。

https://developer.amazon.com/home.html

你需要点击“Alexa Voice Service”。然后创建一个device。

名字我就叫teddy echo，id叫teddy_echo。

其他的尽量跟官方教程一致。

然后点击下一步，需要创建一个profile。

我把name和description都写成。

```
teddy echo security profile
```

然后会得到Security Profile ID、client ID、Client Secret。保存下来。

然后填入Allowed Origin和Allowed return URLs。

然后点击生成。



然后是使能你的Security Profile。

https://developer.amazon.com/lwa/sp/overview.html

选择我们创建的Profile，然后consent url随便填写。这个网址都不一定存在。

```
http://example.com
```



上面的步骤，我们得到了client id、client secret、Profile。

#在树莓派上安装依赖的东西

然后就需要在树莓派上安装AVS SDK的依赖的东西。

配置目录。我们把需要下载的代码都放在/home/pi/sources目录。

```
echo "export SOURCE_FOLDER=$HOME/sources" >> $HOME/.bash_aliases
echo "export LOCAL_BUILD=$HOME/local-builds" >> $HOME/.bash_aliases
echo "export LD_LIBRARY_PATH=$HOME/local-builds/lib:$LD_LIBRARY_PATH" >> $HOME/.bash_aliases
echo "export PATH=$HOME/local-builds/bin:$PATH" >> $HOME/.bash_aliases
echo "export PKG_CONFIG_PATH=$HOME/local-builds/lib/pkgconfig:$PKG_CONFIG_PATH" >> $HOME/.bash_aliases
source $HOME/.bashrc
mkdir $SOURCE_FOLDER
```



1、安装基本工具。

```
sudo apt-get install git gcc cmake build-essential
```

2、

源代码编译nghttp2 。

```
cd $SOURCE_FOLDER
wget https://github.com/nghttp2/nghttp2/releases/download/v1.0.0/nghttp2-1.0.0.tar.gz
tar xzf nghttp2-1.0.0.tar.gz
```

查看我的openssl版本。

```
pi@raspberrypi:~/sources/nghttp2-1.0.0$ openssl version -a
OpenSSL 1.0.1t  3 May 2016
built on: Fri Jan 27 22:44:27 2017
platform: debian-armhf
```

版本够新了。我就不从源代码编译了。

编译安装libcurl。

```
cd $SOURCE_FOLDER
wget https://curl.haxx.se/download/curl-7.50.2.tar.gz
tar xzf curl-7.50.2.tar.gz
cd *curl*/
./configure --with-ssl=$LOCAL_BUILD --with-nghttp2=$LOCAL_BUILD --prefix=$LOCAL_BUILD
make -j3
sudo make install
```

安装sqlite。apt-get安装就好了。我之前有安装。

接下来是gstreamer相关的。之前我虽然安装过，但是可能没有安装完整。

现在完全按照教程下载编译。

```
sudo apt-get install libfaad-dev libsoup2.4-dev libgcrypt20-dev
```

gstreamer 

```
cd $SOURCE_FOLDER
wget https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-1.10.4.tar.xz
tar xf gstreamer-1.10.4.tar.xz
cd *gstreamer*/
./configure --prefix=$LOCAL_BUILD
make -j3
sudo make install
```

gst-plugins-base

```
cd $SOURCE_FOLDER
wget https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-1.10.4.tar.xz
tar xf gst-plugins-base-1.10.4.tar.xz
cd *gst-plugins-base*/
./configure --prefix=$LOCAL_BUILD
make -j3
sudo make install
```

gst-libav-1.10.4

```
cd $SOURCE_FOLDER
wget https://gstreamer.freedesktop.org/src/gst-libav/gst-libav-1.10.4.tar.xz
tar xf gst-libav-1.10.4.tar.xz
cd *gst-libav*/
./configure --prefix=$LOCAL_BUILD
make -j3
sudo make install
```

gst-plugins-good

```
cd $SOURCE_FOLDER
wget https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-1.10.4.tar.xz
tar xf gst-plugins-good-1.10.4.tar.xz
cd *gst-plugins-good*/
./configure --prefix=$LOCAL_BUILD
make -j3
sudo make install
```

gst-plugins-bad

```
cd $SOURCE_FOLDER
wget https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-1.10.4.tar.xz
tar xf gst-plugins-bad-1.10.4.tar.xz
cd *gst-plugins-bad*/
./configure --prefix=$LOCAL_BUILD
make -j3
sudo make install
```

这一步总是报错。应该是SDL的版本不对。

```
SDL_CFLAGS = -D_GNU_SOURCE=1 -D_REENTRANT -I/usr/local/include/SDL
SDL_CLUTTER =
SDL_CONFIG =
SDL_LIBS = -L/usr/local/lib -Wl,-rpath,/usr/local/lib -lSDL -lpthread
```

我先跳过bad这个。



编译portaudio。这个是提供简单的api，来录音和播放音频的。

```
cd $SOURCE_FOLDER
wget http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
tar xf pa_stable_v190600_20161030.tgz
cd *portaudio*/
./configure --prefix=$LOCAL_BUILD
make -j3
sudo make install
```

安装Sensory相关的。

```
sudo apt-get -y install libasound2-dev
sudo apt-get -y install libatlas-base-dev
sudo ldconfig
```



感觉上面的方式走不下去了。

我参考这篇文章，这个是直接执行一个脚本的。看看怎么样。

https://github.com/alexa/avs-device-sdk/wiki/Raspberry-Pi-Quick-Start-Guide-with-Script

也走不通。

算了。我还是在我的笔记本上弄算了。实在是太浪费时间了。



我还是用树莓派重新在一个新的U盘上完全从头搭建一遍。

当前的环境已经有点混乱了。

Jessie的版本。带图形界面的。

我板端安装vnc。来远程连接访问图形界面。

https://github.com/alexa/avs-device-sdk/wiki/Raspberry-Pi-Quick-Start-Guide-with-Script

这个还是走不通。因为脚本执行总是出错。是因为国内的网络环境导致的。

我手动修改脚本里的内容看看。

更新Raspbian到最新版本。

```
Raspbian Stretch Lite
Minimal image based on Debian Stretch
Version: April 2018
Release date: 2018-04-18
Kernel version: 4.14
Release notes: Link
```



我看看是否有现成的镜像可以直接安装体验的。



# 参考资料

1、Raspberry Pi Quick Start Guide。树莓派上搭建echo官方教程。

https://github.com/alexa/avs-device-sdk/wiki/Raspberry-Pi-Quick-Start-Guide/a5646fc9e6dde8128c940b86a9bbece7f65c1ace