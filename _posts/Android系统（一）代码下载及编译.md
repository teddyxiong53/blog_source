---
title: Android系统（一）
date: 2018-01-22 19:42:04
tags:
	- Android系统

---



这个系列文章，是要分析一下Android系统的整体结构。

# 获取Android源代码

鉴于GFW的阻挡，从墙外下载无疑是不可取。不过因为这个需求很大，所以国内有很多镜像网站。

找了不少的文章，都是说用清华大学的镜像源。好吧。我就用这个吧。

1、安装repo。

```
sudo apt-get install repo
```

这个实际上是一个Python脚本。

2、修改/usr/bin/repo文件。把REPO_URL替换为下面这个。

```
REPO_URL = 'https://gerrit-google.tuna.tsinghua.edu.cn/git-repo'
```

3、下载。要指定一个版本。我看的书是5.0的，所以为了环境统一，我使用5.0的版本。

```
repo init -u https://aosp.tuna.tsinghua.edu.cn/platform/manifest -b android-5.0.0_r1
```

开始同步：

```
repo sync -j4
```

2018年1月22日19:55:53

现在开始。过1个小时看看如何。

代码非常多。我看下载到11G还没有下载完成。

https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/

首次

# 源代码目录分析

1、abi。应用程序二进制接口。

2、art。全新的运行环境。

3、bonic。bonic C库。

4、bootable。启动代码。

5、build。编译规则放这里。

6、cts。兼容性测试套件。

7、dalvik。虚拟机。

8、development。应用开发相关。

9、device。设备相关代码。

10、docs。文档。

11、external。开源模块。

12、frameworks。核心框架。

13、gdk。即时通信模块。

14、hardware。hal代码。

15、kernel。linux内核代码。

16、libcore。核心库。

17、libnativehelper。JNI库的基础。

18、ndk。

19、out。编译的输出东西放这里。

20、packages。应用程序包。

21、pdk。本地开发套件。

22、prebuilt。

23、sdk。

24、system。

25、tools。工具文件夹。

26、vendor。厂家代码。

27、Makefile。全局Makefile。



# 系统分层

系统分为应用层、应用框架层。

现在看看分层和上面这些目录的对应关系。

## 应用层（packages目录）

1、apps。存放了官方的应用。

2、experimental。非官方的应用。

3、inputmethods。

4、providers。

5、screensavers。

6、wallpapers。

## 应用框架层（frameworks目录）



## 系统程序库

1、系统C库。

2、媒体库。

3、图层显示库。

4、网络引擎库。

5、3D图形库。

6、sqlite。

## hal层



#接口分类

我们可以把Android源代码编译出一个SDK，这个SDK的功能跟我们另外下载的SDK包的功能是一样的。而且比单独的SDK的功能还要多一些。

SDK的接口有暴露接口和隐藏接口。

哪些接口是隐藏接口呢？例如统计WiFi和蓝牙打开时间这种功能，在SDK里就没有直接的接口可以调用。另外电池消耗信息，也是隐藏接口才能做到。

就以电池这个为例，在`frameworks/base/core/java/android/os`目录下，存在BatteryStats.java和BatteryStatsImpl.java这2个文件。这里面的很多函数都被加上了@hide标签。不过一般也尽量少用隐藏接口。谷歌不推荐，出问题也不负责的。

这些接口的调用举例。在设置里，一般有个各个应用的耗电情况统计。对应的文件是PowerUsageSummary.java。放在`packages/apps/settings/src/com/android/settings/fuelgauge`目录下。



# 编译源代码

参考这篇文章：

http://blog.csdn.net/fuchaosz/article/details/51487585

1、安装jdk。我的电脑是Ubuntu16.04，默认带了openjdk的1.8的版本。

2、安装编译需要的工具。

```
sudo apt-get install -y git flex bison gperf build-essential libncurses5-dev:i386 
sudo apt-get install libx11-dev:i386 libreadline6-dev:i386 libgl1-mesa-dev g++-multilib 
sudo apt-get install tofrodos python-markdown libxml2-utils xsltproc zlib1g-dev:i386 
sudo apt-get install dpkg-dev libsdl1.2-dev libesd0-dev
sudo apt-get install git-core gnupg flex bison gperf build-essential  
sudo apt-get install zip curl zlib1g-dev gcc-multilib g++-multilib 
sudo apt-get install libc6-dev-i386 
sudo apt-get install lib32ncurses5-dev x11proto-core-dev libx11-dev 
sudo apt-get install lib32z-dev ccache
sudo apt-get install libgl1-mesa-dev libxml2-utils xsltproc unzip m4
```

```
make -j256
```

默认编译目标是可运行的镜像。

在模拟器运行。

```
emulator
```

如果要编译sdk，则命令是：

```
make sdk
```





