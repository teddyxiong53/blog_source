---
title: aosp（1）
date: 2018-11-04 11:00:02
tags:
	- Android

---



AOSP是Android Open Source Project的缩写。

1、是谷歌领导的Android开源工程。

2、AOSP可以理解为原生Android。

3、注意原生ROM和AOSP的区别是：AOSP里没有集成谷歌服务。

4、**AOSP不包含任何驱动程序，需要你自己将驱动整合进去编译。**



广义的原生ROM可以理解为AOSP集成了GMS（Google Mobile Service）之后得到的ROM。

GMS包括：谷歌搜索、Gmail、谷歌地图、Google+、谷歌日历、Google Play。

要想体验原生Android，有三种途径：

1、nexus和pixel手机。谷歌”亲儿子“。

2、Google Play Edition。谷歌“干儿子”。谷歌针对性地在原生ROM里支持一些厂家的旗舰机。

3、民间自己移植的。





```
sudo apt install autoconf gcc-aarch64-linux-gnu libaio-dev libbluetooth-dev libbrlapi-dev libbz2-dev libcap-dev libcap-ng-dev libcurl4-gnutls-dev libepoxy-dev libfdt-dev libgbm-dev libgles2-mesa-dev libglib2.0-dev libibverbs-dev libjpeg8-dev liblzo2-dev libncurses5-dev libnuma-dev librbd-dev librdmacm-dev libsasl2-dev libsdl1.2-dev libsdl2-dev libseccomp-dev libsnappy-dev libssh2-1-dev libtool libusb-1.0-0 libusb-1.0-0-dev libvde-dev libvdeplug-dev libvte-2.90-dev libxen-dev valgrind xfslibs-dev xutils-dev zlib1g-dev
```

这个会报错。

```
Package libvte-2.90-dev is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source

E: Package 'libvte-2.90-dev' has no installation candidate
```

网上查了下，好像是libvte-2.90-dev不再提供，要用libvte-2.91-dev

改了试一下。

```
sudo apt install autoconf gcc-aarch64-linux-gnu libaio-dev libbluetooth-dev libbrlapi-dev libbz2-dev libcap-dev libcap-ng-dev libcurl4-gnutls-dev libepoxy-dev libfdt-dev libgbm-dev libgles2-mesa-dev libglib2.0-dev libibverbs-dev libjpeg8-dev liblzo2-dev libncurses5-dev libnuma-dev librbd-dev librdmacm-dev libsasl2-dev libsdl1.2-dev libsdl2-dev libseccomp-dev libsnappy-dev libssh2-1-dev libtool libusb-1.0-0 libusb-1.0-0-dev libvde-dev libvdeplug-dev libvte-2.91-dev libxen-dev valgrind xfslibs-dev xutils-dev zlib1g-dev
```

果然就可以了。

设置环境变量。

```
export PROJECT_PATH="/home/teddy/work2/aosp/qemu_android"
export VIRGLRENDERER_PATH="${PROJECT_PATH}/virglrenderer"
export QEMU_PATH="${PROJECT_PATH}/qemu"
export LINUX_PATH="${PROJECT_PATH}/linux"
export ANDROID_PATH="${PROJECT_PATH}/android"
export ANDROID_TOOLS_PATH="${PROJECT_PATH}/android-tools"
```

下载编译virglrenderer。这个是用来支持图形渲染的。

https://github.com/freedesktop/virglrenderer

不大，就1M多。

编译：

```
./autogen.sh
make
sudo make install
```

qemu的我是已经安装好的。所以先不安装。

下载内核，看教程写的是，git取最新版本。

我就直接下载最新版本的压缩包就好了。

https://github.com/torvalds/linux

现在内核源码接近200M了。

```
wget http://memcpy.io/files/2016-08-30/Kconfig -O ${LINUX_PATH}/.config
make oldconfig
make -j
```

这种配置方式，对我当前已经行不通了。

但是作者给出一些配置参考。我只要保证对应的配置是对的就好了。

当前内核版本是4.19的。



如果安装了多个版本的java。用这个命令来选择。

```
teddy@teddy-ubuntu:~/work2/aosp/qemu_android/android$ sudo update-alternatives --config java
There are 2 choices for the alternative java (providing /usr/bin/java).

  Selection    Path                                            Priority   Status
------------------------------------------------------------
* 0            /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java   1081      auto mode
  1            /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java   1081      manual mode
  2            /usr/lib/jvm/jdk1.6.0_45/bin/java                300       manual mode

Press <enter> to keep the current choice[*], or type selection number: 0
```

我选择为0 。

javac的同样要选。

```
 sudo update-alternatives --config javac
```



先不管前面的了。现在直接下载aosp的代码。

```
teddy@teddy-ubuntu:~/work2/aosp/qemu_android/android$ git config --global user.name "teddyxiong53"
teddy@teddy-ubuntu:~/work2/aosp/qemu_android/android$ git config --global user.email "teddyxiong53@gmail.com"
teddy@teddy-ubuntu:~/work2/aosp/qemu_android/android$ 
teddy@teddy-ubuntu:~/work2/aosp/qemu_android/android$ repo init -u https://android.googlesource.com/platform/manifest
```

昨晚下载了一晚上，早上起来看，发现repo sync出错退出了。真的坑。

用这个脚本，如果repo sync出错退出，重新执行。

```
#!/bin/sh

repo sync
while [ $? -ne 0  ]; do
    repo sync
done
```

晚上我的vps下载速度可以到2M左右。白天只有300K左右。

放着慢慢下吧。



现在从这里下载打包好的aosp-20160806.tar。大概15G。

https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/

下载完之后，解压，执行repo sync -l。报了下面的错误。

```
for line in d.decode('utf-8').rstrip('\0').split('\0'):  # pylint: disable=W1401
```

直接改对应的python文件里，把`decode('utf-8')`去掉。

再执行就可以了。

# 编译

```
source build/envsetup.sh
```

打印了这些：

```
including device/asus/deb/vendorsetup.sh
including device/asus/flo/vendorsetup.sh
including device/asus/fugu/vendorsetup.sh
including device/generic/mini-emulator-arm64/vendorsetup.sh
including device/generic/mini-emulator-armv7-a-neon/vendorsetup.sh
including device/generic/mini-emulator-mips/vendorsetup.sh
including device/generic/mini-emulator-x86_64/vendorsetup.sh
including device/generic/mini-emulator-x86/vendorsetup.sh
including device/htc/flounder/vendorsetup.sh
including device/huawei/angler/vendorsetup.sh
including device/lge/bullhead/vendorsetup.sh
including device/lge/hammerhead/vendorsetup.sh
including device/linaro/hikey/vendorsetup.sh
including device/moto/shamu/vendorsetup.sh
including sdk/bash_completion/adb.bash
```

执行执行lunch命令。

选择mini_emulator_x86_64-userdebug，网上看说这个在笔记本上测试起来方便点。

-eng:代表engineer,也就是所谓的开发工程师的版本,拥有最大的权限(root等),此外还附带了许多debug工具

那还是选择aosp_x86_64-eng这个吧。

然后make -j4 开始编译。

-j后面的数字，是你电脑核心数乘以2比较合适。

```
Your version is: /bin/bash: javac: 未找到命令.
The required version is: "1.8"
```

```
sudo apt-get install openjdk-8-jdk
```



在我的笔记本上是编译不过的。还是电脑性能太低了，内存太小了。总是jack出问题，要么是java虚拟机内存太小。

最后我在台式机上的虚拟机里编译过了。给虚拟机分配了10G的内存。jvm给了8G的内存。

```
export JACK_SERVER_VM_ARGUMENTS="-Dfile.encoding=UTF-8 -XX:+TieredCompilation -Xmx8g"
./prebuilts/sdk/tools/jack-admin kill-server
./prebuilts/sdk/tools/jack-admin start-server
```

在台式机上很顺利编译过了，几个小时就完成了。

在虚拟机里是无法运行的。

```
hlxiong@hlxiong-VirtualBox:~/work3/aosp$ emulator
emulator: WARNING: system partition size adjusted to match image file (1280 MB > 200 MB)

emulator: WARNING: data partition size adjusted to match image file (550 MB > 200 MB)

emulator: WARNING: Increasing RAM size to 1GB
emulator: ERROR: x86_64 emulation currently requires hardware acceleration!
Please ensure KVM is properly installed and usable.
CPU acceleration status: KVM is not installed on this machine (/dev/kvm is missing).
```



看看怎么在物理机里运行编译出来的镜像。



看一下build/envsetup.sh脚本内容。

```
第一个函数是：
function hmm()
这个是打印帮助信息。
Invoke ". build/envsetup.sh" from your shell to add the following functions to your environment:
```

```
- m:         Makes from the top of the tree.
- mm:        Builds all of the modules in the current directory, but not their dependencies.
- mmm:       Builds all of the modules in the supplied directories, but not their dependencies.
             To limit the modules being built use the syntax: mmm dir/:target1,target2.
- mma:       Builds all of the modules in the current directory, and their dependencies.
- mmma:      Builds all of the modules in the supplied directories, and their dependencies.
```



# 编译过程分析

看main.mk文件。

这个表示什么意思？RCS是一个很老的版本管理软件。

现在相当于禁止这个的意思。

```
# this turns off the RCS / SCCS implicit rules of GNU Make
% : RCS/%,v
% : RCS/%
```

使用make编译，则编译的相关脚本在这个目录下。

```
BUILD_SYSTEM := $(TOPDIR)build/core
```

默认目标：

```
# This is the default target.  It must be the first declared target.
.PHONY: droid
DEFAULT_GOAL := droid
$(DEFAULT_GOAL): droid_targets
```

默认会这样：

```
Running kati to generate build-aosp_x86_64.ninja.
```

这个ninja文件会有几百M。

整个main.mk，都被这个变量判断包含了。

```
	Line 100: ifndef KATI
	Line 108: else # KATI
	Line 1136: endif # KATI
```

默认不会去编译模拟器。

```
ifndef BUILD_EMULATOR
  # Emulator binaries are now provided under prebuilts/android-emulator/
  BUILD_EMULATOR := false
endif
```

jack是用来编译java的。

```
#
# -----------------------------------------------------------------
# Install and start Jack server
-include $(TOPDIR)prebuilts/sdk/tools/jack_server_setup.mk
```

是不是要编译sdk。

```
is_sdk_build :=

ifneq ($(filter sdk win_sdk sdk_addon,$(MAKECMDGOALS)),)
is_sdk_build := true
endif
```



```
FULL_BUILD := true
```

包含所有的Makefile。

```
#
# Include all of the makefiles in the system
#

subdir_makefiles := $(SOONG_ANDROID_MK) $(call first-makefiles-under,$(TOP))

$(foreach mk,$(subdir_makefiles),$(info including $(mk) ...)$(eval include $(mk)))

```

总的文件，是在aosp/out/soong/Android-aosp_x86_64.mk里。

这里面可以看到这样的，这就是要编译的模块了。

```
	Line 302: LOCAL_PATH := hardware/libhardware/modules/audio
	Line 320: LOCAL_PATH := hardware/libhardware/modules/audio
	Line 338: LOCAL_PATH := hardware/libhardware/modules/audio
	Line 356: LOCAL_PATH := hardware/libhardware/modules/audio
	Line 374: LOCAL_PATH := bionic/benchmarks
	Line 391: LOCAL_PATH := bionic/benchmarks
	Line 409: LOCAL_PATH := bionic/tests
	Line 426: LOCAL_PATH := bionic/tests
	Line 443: LOCAL_PATH := bionic/tests
```



# 编译调试单个模块

例如，我们在Launcher2的onCreate里加了一句打印，想把这个改动在整机上进行测试。

应该怎样操作呢？

```
mmm packages/apps/Launcher2
```

编译完会提示你install到哪个位置了。

```
out/target/product/generic_x86_64/data/app/LauncherRotationStressTest/LauncherRotationStressTest.apk
```



```
adb remount
adb shell rm system/priv-app/Launcher2/Launcher2.apk
adb shell rm -r system/priv-app/Launcher2/arm
adb push /home/lxf/Launcher2.apk system/priv-app/Launcher2
adb reboot
```



# 简介

AOSP（Android Open Source Project）是由Google推动的开放源代码项目，旨在开发和维护Android操作系统。

它提供了一个完整的软件堆栈，包括操作系统、中间件和关键应用程序，供设备制造商、开发者和个人用户使用。

AOSP的主要组成部分包括：

1. Android操作系统：AOSP提供了Android的基本操作系统框架，包括核心系统服务、硬件抽象层（HAL）、设备驱动程序等。

2. 中间件：AOSP包括了一系列中间件组件，如图形库、多媒体框架、SQLite数据库、Web浏览器引擎等，为开发者提供了丰富的功能支持。

3. 应用程序：AOSP中包含了一些基本的应用程序，如电话、联系人、短信、浏览器等，这些应用程序的源代码都是公开的，可以用于定制和开发。

AOSP的开放性使得各个厂商和开发者可以基于其源代码进行定制和开发，从而创建出适用于不同设备和场景的Android系统。同时，AOSP也是Android生态系统的核心，为数以亿计的Android设备提供了稳定的基础。

# 发展历史

AOSP的发展历史可以追溯到2007年，当时Google宣布推出Android操作系统。以下是AOSP的主要发展里程碑：

1. **2007年11月：** Google宣布Android项目，并发布了早期版本的软件开发工具包（SDK）。

2. **2008年9月：** 首个基于AOSP的Android版本，即Android 1.0，面向开发者发布。这个版本主要面向早期的开发者和手机制造商。

3. **2009年10月：** 随着Android 2.0（代号：Eclair）的发布，AOSP开始变得更加成熟和功能丰富。Eclair引入了多个重要功能，包括Google Maps导航、Web浏览器改进、Exchange支持等。

4. **2010年：** Android 2.2（代号：Froyo）发布，引入了一系列性能优化和新功能，如移动热点、Adobe Flash支持等。

5. **2011年10月：** Android 4.0（代号：Ice Cream Sandwich）发布，标志着Android手机和平板电脑的统一。Ice Cream Sandwich引入了全新的用户界面设计，以及一系列改进的功能和API。

6. **2012年7月：** Android 4.1（代号：Jelly Bean）发布，带来了更流畅的用户体验、Google Now助手、可扩展通知系统等功能。

7. **2014年6月：** Android 4.4（代号：KitKat）发布，着重优化了系统性能，使得更老旧的设备也能够运行流畅，并引入了全新的运行时环境ART（Android Runtime）。

8. **2015年：** Android 6.0（代号：Marshmallow）发布，引入了诸多安全和隐私改进，如指纹识别支持、运行时权限等。

9. **2017年：** Android 8.0（代号：Oreo）发布，引入了更多的性能优化、背景限制和通知改进，以及全新的项目Treble，旨在简化Android系统的更新和定制。

10. **2019年：** Android 10发布，标志着Android正式摒弃了甜点命名法，以版本号命名。Android 10引入了暗黑模式、全新的手势导航、隐私控制等功能。

11. **2020年：** Android 11发布，继续加强隐私保护、改善消息管理和设备控制，引入了Bubbles功能等。

12. **2021年：** Android 12发布，带来了全新的用户界面设计语言Material You、更强大的隐私控制、更快的性能等特性。

这些只是AOSP发展历史中的一部分重要里程碑，随着时间的推移，AOSP不断演进，持续为Android生态系统带来创新和改进。

# aosp的构建系统说明

AOSP的构建系统是一个复杂但高度灵活的工具链，用于将源代码转换为可执行的Android系统。它主要基于GNU Make和一些自定义的构建脚本，以及一系列工具和脚本来处理源代码、编译、链接和打包。

以下是AOSP构建系统的一些关键组成部分和说明：

1. **Makefile和Blueprints：** AOSP的构建系统主要使用Makefile来定义构建规则和任务。每个模块（如应用程序、库、设备驱动程序等）都有自己的Makefile来描述其构建过程。另外，AOSP引入了Blueprints，这是一种用于描述模块依赖关系和构建配置的声明性语言，它可以用来生成Makefile。

2. **Soong：** Soong是AOSP的新一代构建系统，取代了以前的基于Makefile的系统。Soong使用Blueprints语言来描述模块的构建配置和依赖关系，然后生成Ninja build文件来实际执行构建任务。它更灵活、高效，并提供了更好的并行构建支持。

3. **Ninja：** Ninja是一个快速的构建系统，用于执行生成的构建任务。当使用Soong构建AOSP时，它会生成Ninja build文件，然后使用Ninja来并行执行编译、链接等任务，加快构建速度。

4. **源代码处理工具：** AOSP的构建系统包括一系列工具和脚本来处理源代码，例如`repo`工具用于管理多个Git仓库、`m`工具用于执行构建任务、`mm`用于构建单个模块等。

5. **模块化：** AOSP的构建系统是模块化的，每个模块都有自己的构建规则和依赖关系。这使得开发者可以方便地添加、移除或替换系统中的各个组件，从而定制Android系统以满足特定需求。

总的来说，AOSP的构建系统是一个功能强大且高度可定制的工具链，为开发者提供了构建和定制Android系统的灵活性和便利性。

# 参考资料

1、Building Android for Qemu: A Step-by-Step Guide

https://www.collabora.com/news-and-blog/blog/2016/09/02/building-android-for-qemu-a-step-by-step-guide/

2、Android-x86虚拟机安装配置全攻略

https://cleanli.github.io/cleanhome/posts/2017-06-07/Android_x86_debug_config.html

3、源码编译运行android emulator

https://www.cnblogs.com/wxishang1991/p/5680297.html

4、

https://source.android.com/source/downloading

5、android framework之旅（三）编译调试单个模块

https://www.jianshu.com/p/d758646cac80

6、

https://www.jianshu.com/p/6b2de1c4a1bc