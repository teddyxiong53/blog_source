---
title: yodaos（1）
date: 2022-08-09 19:15:08
tags:
	- yodaos

---

--

# 介绍

YodaOS 是一个基于 Linux 的开源操作系统，专门设计用于智能音箱、智能家居设备和其他物联网设备。它由中国的一家技术公司团队开发，旨在为物联网设备提供一个灵活、可扩展、安全且高效的操作系统。

YodaOS 采用了基于声音的用户界面，即用户可以通过语音指令与设备进行交互。它支持多种语音助手，例如 Yoda AI，可以执行各种任务，包括播放音乐、控制家居设备、提供天气信息等等。

YodaOS 的设计注重了安全性和隐私保护，它提供了多种安全功能，如固件加密、权限管理和隐私控制，以确保用户数据的安全性。

此外，YodaOS 还具有良好的可定制性和可扩展性，开发者可以根据自己的需求定制和扩展系统功能，使其适应不同类型的物联网设备。

总的来说，YodaOS 是一个面向物联网设备的先进操作系统，通过其声音交互界面、安全性和可扩展性，为智能音箱和其他智能设备提供了强大的基础。

# 编译

**解决办法**：这些都是同样类型的错误，修复方法是#include<sys/sysmacros.h>添加到ismounted.c，devname.c，debugfs.c，create_inode.c文件中



```
error: conflicting types for 'copy_file_range'
```

https://blog.csdn.net/ThinkAboutLife/article/details/109183880

解决了上面的，又报了这个。

```
/usr/bin/ld: create_inode.c:(.text+0x2d4): undefined reference to `minor'
```

再加上`#include<sys/sysmacros.h>`。继续编译，现在报这个：

```
debugfs.c:(.text+0x4310): undefined reference to `makedev'
```

这些问题应该是我的Ubuntu版本是20.04导致的。

版本问题确实挺麻烦的。

解决不过来。直接在18.04上编译看看。

也是一样碰到错误。

难道只能在16.04上编译通过？

那就弄一个docker进行编译。

```
 docker pull ubuntu:16.04
```

https://blog.csdn.net/bryanwang_3099/article/details/107345248

参考这篇来做。

```
//创建容器
docker run -itd --name ubuntu1604 --privileged=true -p 9022:22  -v /home/amlogic/work:/work ubuntu:16.04

//进入容器
docker exec -it ubuntu1604 /bin/bash
```

现在可以进入容器，在容器里安装需要的基本工具。

从这里的readme拿到要安装的工具列表。

https://github.com/yodaos-project/yodaos

首先碰到的问题，就是docker里安装工具提示找不到：

```
E: Unable to locate package vim
```

需要先apt-get update一下。就可以安装了。

工具安装好了。

现在配置提示：

```
version `GLIBC_2.27' not found (required by scripts/config/conf)
```

这个又说是要升级到18.04才行。

算了，不搞了。

或者是我自己把相关代码移植到一个可以编译的openwrt上来。

或者就是在A113X2的基础上做这个。

我觉得可以做。

另外发现rokid的开放平台那边的文档还比较值得一读。

https://developer.rokid.com/docs/5-enableVoice/rokid-vsvy-sdk-docs/yodaosSystem/general/YodaOS_Build_Environment.html

从这里用repo的方式同步代码。

代码同步完成后，直接source envsetup.sh，选择树莓派的，然后make -j1 V=s进行编译。

```
freadahead.c:91:3: error: #error "Please port gnulib freadahead.c to your platform! Look at the definition of fflush, fread, ungetc on your system, then report this to bug-gnulib."
   91 |  #error "Please port gnulib freadahead.c to your platform! Look at the definition of fflush, fread, ungetc on your system, then report this to bug-gnulib."
      |   ^~~~~
```

解决方法：

到openwrt目录下：

```
$ output/build/host-m4-1.4.17
$ sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
$ echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
$ make
```



https://steward-fu.github.io/website/handheld/trimui/fix_m4.htm

有碰到问题。

```
error: #error "Please port gnulib fseterr.c to your platform!
```

参考这个

https://steward-fu.github.io/website/handheld/trimui/fix_bison.htm

```
$ vim output/build/host-bison-3.0.4/lib/stdio-impl.h +20
  #if !defined _IO_IN_BACKUP && defined _IO_EOF_SEEN
  # define _IO_IN_BACKUP 0x100
  #endif

$ vim output/build/host-bison-3.0.4/lib/fseterr.c +32
  #if defined _IO_EOF_SEEN || __GNU_LIBRARY__ == 1 /* GNU libc, BeOS, Haiku, Linux libc5 */
```

解决了。继续编译。

出错：

```
devname.c:(.text+0x888): undefined reference to `makedev'
/usr/bin/ld: devname.c:(.text+0xb7e): undefined reference to `makedev'
```

解决

```
vim build_dir/host/e2fsprogs-1.42.8/lib/blkid/devname.c 中添加 #include <sys/sysmacros.h>
```

改了编译继续报错。

这么改：

```
vim build_dir/host/mtd-utils-1.5.1/mkfs.jffs2.c 中添加 #include <sys/sysmacros.h>
vim build_dir/host/mtd-utils-1.5.1/ubi-utils/libubi.c  中添加 #include <sys/sysmacros.h>
vim build_dir/host/mtd-utils-1.5.1/mkfs.ubifs/devtable.c 中添加 #include <sys/sysmacros.h>
vim build_dir/host/mtd-utils-1.5.1/mkfs.ubifs/mkfs.ubifs.c 中添加 #include <sys/sysmacros.h>
```

出错

```
./../misc/create_inode.c:395:18: error: conflicting types for 'copy_file_range'
```

参考这个，

https://blog.csdn.net/ThinkAboutLife/article/details/109183880

包minor这样的错误的，都是要加\#include<sys/sysmacros.h>头文件。

出错：

```
error: dereferencing pointer to incomplete type 'RSA' {aka 'struct rsa_st'}
```

参考这个

https://blog.csdn.net/rainforest_c/article/details/82722333

是openssl的版本问题。

但是有点难搞。

https://github.com/openwrt/openwrt/commit/70b104f98c0657323b28fce140b73a94bf3eb756?diff=unified

从这里把内容保存成patch文件。

放到yodaos-repo/openwrt/build_dir/host/u-boot-2014.10目录下。

执行：

```
patch -p1 < fix-openssl.patch 
```

可以打上补丁。

然后这个编译错误就解决了。

find-util报错。

```
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h

sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' gl/lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> gl/lib/stdio-impl.h
echo "#define _IO_ferror_unlocked" >> gl/lib/stdio-impl.h
sed -i '/unistd/a #include <sys/sysmacros.h>' gl/lib/mountlist.c
```

报错：

```
cmcurl/lib/vtls/openssl.c:2482:13: error: dereferencing pointer to incomplete type 'X509' {aka 'struct x509_st'}
```

到这里找patch。

https://git.openwrt.org/?p=openwrt/openwrt.git;a=tree;f=tools/mkimage/patches;h=ee5e92e913e487f63a5d8a82ebd43ccdd7b0a3f7;hb=70b104f98c0657323b28fce140b73a94bf3eb756

这个其实跟我之前的一样。

这个是cmake要打。

但是cmake目录下找不到这个文件。

find -name rsa-sign.c

不用手动打patch。

而是放到tools/mkimage/patchs/目录下。

这篇文章提到的打这些patch的方法的。

https://blog.csdn.net/zmlovelx/article/details/80904109

但是当前的方法不能解决cmake里的这个错误。

看看openssl降级怎么做。

https://www.cnblogs.com/linagcheng/p/15870060.html

但是这个很容易把环境弄乱。

我把cmake改成3.19.1的，因为我们的sdk就是这个版本。

编译报错。

```
Unknown option: CPPFLAGS=-I/mnt/fileroot/hanliang.xiong/work/yodaos-repo/openwrt/staging_dir/host/include -I/mnt/fileroot/hanliang.xiong/work/yodaos-repo/openwrt/staging_dir/host/usr/include 
```

https://www.codeleading.com/article/87655954453/

直接把对应的die去掉。

继续编译。

错误确实太多了。但是尽量坚持到最后。

现在cmake的问题通过替换版本解决了。

报错：这个老问题了。

```
mksquashfs.c: In function 'create_inode':
mksquashfs.c:987:24: error: called object 'major' is not a function or function pointer
```

改了这些。

host的编译终于过了。

开始编译target的内容。

还是报错

```
gdbusauth.c: In function '_g_dbus_auth_run_server':
gdbusauth.c:1304:11: error: '%s' directive argument is null [-Werror=format-overflow=]
```

参考这个

https://cloud.tencent.com/developer/article/1882510

找到报错的位置，加一个NULL判断。

还好这种不多，而且的确是打印的NULL了。



编译shadownode又报错。说libmqtt没有。

代码是有，但是不知道为什么没有编译。

我配置为最小编译看看。

还是要找libmqtt。

```
make[5]: *** No rule to make target 'lib/libmqtt_packet.a', needed by 'lib/libiotjs.so'.  Stop.
```

我再把cmake里对mqtt的依赖去掉。

可以编译过了。现在又看到有mqtt的库了。

可能是顺序问题。

2022年8月12日23:41:47

终于编译完成了。



把开机脚本看一下。

看/etc/rc.d/S92lightd里，这个是最先开始使用iotjs的。

模块之所以可以require找到，就是在

```
/usr/lib/node_modules/ 
```

这个目录下。

所以这样可以require找到：

```
require('@yoda/oh-my-little-pony')
```



我现在最大的疑问，就是开机启动了哪些进程。

怎么把js运行时环境跑起来的？怎么把那一堆的json文件解析调用的？

怎么把模块进行查找导入的？

# 术语表

有不少概念是rokid自己创造的，不是通用的概念。

所以有必要把这些概念梳理一遍，这样看代码就心里会清楚一些。

## flora

rokid自己写的ipc机制，作为系统的默认ipc机制。

## protocol Fauna

yodaos的运行时协议。

文档在这里：

https://github.com/yodaos-project/yoda.js/blob/master/docs/protocol-fauna.md

Fauna协议是用来让js应用和其他语言的应用进行通信。

进程启动

```
yodaos.fauna.status-report
	让进程报告自己的状态。状态有两种：ready、alive。
	 ANR(Application Not Responding)
	 在应用报告ready后，如果在15s内没有报告alive，
	 那么runtime就会发SIGKILL信号去杀掉这个进程。
	 每15秒检测一次alive信号。
	 
```

调用方法

```
yodaos.fauna.invoke
	跟的内容是一个json字符串。
	json的定义是这样：
	interface Invocation {
		'namespace': string
		'method': string
		'params': any[]
	}
	
	返回的结果
	interface ResolveResult {
		'action': 'resolve',
		'result': any
	}
	interface RejectResult {
		'action': 'reject',
		'error': any
	}
	type Result = ResolveResult | RejectResult
```

订阅事件

```
yodaos.fauna.subscribe
	interface Subscription {
		'namespace'?: string
		'event' : string
		'params': any[]
	}
	返回是数组
	
```

Application event harbor（港湾）

```
yodaos.fauna.harboar
	[type, messageJson]
	type分类：event、fatal-error、internal。
	messageJson的组成：
	interface Event {
		'namespace': string,
		'event': string,
		'params': []
	}
	interface FatalError {
		'message': string
	}
	interface Internal {
	
	}
	
```

## Voice Interface Driver

用来对接不同个语音云平台。

相当于一个不同云平台的适配层。

把云平台的基础指令，TTS/ASR、控制指令等转成本地可以理解的YodaOS Message。

## YodaOS Application

每个应用通过YodaOS Message的方式监听消息。

来完成自己的业务逻辑。

内置的应用包括：

cloud-player、system、volume、launcher。

## YodaOS Component

用于连接system framework跟Application framework的组件。

目前的组件列表包括：

app-loader.js

app-launcher.js

audio-focus.js

broadcast.js

chronos.js

dbus-registry.js

dispatcher.js

effect.js

flora.js

keyboard.js

media-controller.js

memory-sentinel.js

permission.js

visibility.js

这些Component的特点是：

```
1、导出一个类。
2、类的构造函数参数是runtime。
```

Component提供了这些核心功能：

1、应用加载。

2、语音焦点。

3、广播。

4、计时器。

5、内存管理。

## YodaOS Message

在YodaOS里的ipc方式，有下面这些：

* YodaOS URL方式。例如：`yoda-app://cloud-player/play-tts-stream`。单向调用的方式，一般用于语音或者硬件指令下发。
* YodaOS Event方式。也是单向的，跟URL的不同在于，Event是使用订阅的方式，支持一对多。
* YodaOS Function。双向。请求响应模型。被调用者要在一定时间内返回值。

上面三种方式，底层都是基于flora的。

## YodaOS Package

系统中的一种软件单元。

包括：

* js文件。
* N-API桥接模块。
* package.json

## YodaOS Runtime

运行时，提供了：

* 系统初始化。
* 应用管理。
* 组件管理。



# flora

https://github.com/yodaos-project/flora

这个是一个进程间的通信机制。

有什么特色？就是rokid的自己写的一个通信模块。

支持pub/sub机制。

mqtt也可以做到吧。

暂时不细看。

可以简单看看。就看include下面的3个头文件。

flora-svc.h ：服务端

flora-cli.h：客户端

flora-agent.h：对客户端的再封装，简化接口。

先从flora-agent.h入手。

这个头文件里提供了c和c++两套接口。

我就看c的接口。

依赖了mutils这个ming的工具类库。

https://github.com/rokid/mingutils

caps这部分是进行序列化的工具。也提供了c和c++两套接口。

把代码取下来编译测试看看。

rokid的代码都是需要先config一下。然后再编译。

```
./config --build-dir=./build --cmake-modules=./cmake-modules --prefix=./install-dir 
cd ./build
make && make install
```

cmake-modules是rokid的一个只有2个文件的cmake配置。

https://github.com/Rokid/CMake-Modules

make install后的路径是这样：

```
.
├── include
│   ├── caps
│   │   └── caps.h
│   ├── log
│   │   └── rlog.h
│   └── misc
│       ├── circle-stream.h
│       ├── clargs.h
│       ├── global-error.h
│       ├── heap-sort.h
│       ├── http.h
│       ├── merge-sort.h
│       ├── strpool.h
│       ├── thr-pool.h
│       ├── uri.h
│       ├── variable_queue.h
│       └── xmopt.h
└── lib
    ├── libcaps.a
    ├── libcaps.so
    ├── libmisc.a
    ├── libmisc.so
    ├── librlog.a
    └── librlog.so

```

到demo目录下，下面没有Makefile。自己写一个，对这些demo进行编译。然后运行看看效果。

```
.PHONY: caps_demo
CFLAGS := -g -I/home/hanliang.xiong/work/test/mingutils/build/install-dir/include/caps \
	-I/home/hanliang.xiong/work/test/mingutils/build/install-dir/include/log \
	-I/home/hanliang.xiong/work/test/mingutils/build/install-dir/include/misc 

LDFLAGS := -L/home/hanliang.xiong/work/test/mingutils/build/install-dir/lib \
	-lmisc -lcaps  -lrlog

all:
	g++ -c caps_demo.cc $(CFLAGS) -o caps_demo.o
	g++ -c random_caps_factory.cc $(CFLAGS) -o random_caps_factory.o
	g++ caps_demo.o random_caps_factory.o $(LDFLAGS) -o caps_demo
```

运行测试：

```
 export LD_LIBRARY_PATH=/home/hanliang.xiong/work/test/mingutils/build/install-dir/lib
 ./caps_demo
```



# wavplayer

这个是一个简单的播放器。可以用这个作为切入口看整个的流程。

c++的实现是在：

frameworks\native\libs\librplayer\include\SimplePlayer.h

frameworks\native\libs\librplayer\src\SimplePlayer.cpp

使用的是pulseaudio的接口来做的。所以系统的音频是靠pulseaudio来统一管理的。

所以接下来看node native的实现。

在这里：

frameworks\jsruntime\packages\@yoda\multimedia\src\WavPlayer.cc

实现有些复杂。

所以js做媒体这一块，问题就在于增加了复杂性。属于费力不讨好的。

js适合做的，应该是自己的业务逻辑，跟复杂模块关联不大的。

不然封装麻烦，调试麻烦，效率低，出问题难以查找。

对于wavplayer本来是个很简单的应用场景，本来也不会有太多的应用组合。



# 灯光分析

这个light逻辑都写得很复杂。也不知道可以应对什么复杂的呈现。

带来了什么配置上的便利。

# frameworks

## jsruntime分析

```
  <project name="Rokid/YodaRT" path="frameworks/jsruntime"
```

YodaRT是yodaos的JavaScript layer。

https://github.com/yodaos-project/yoda.js

这个仓库不完全一样。

提供了下面的功能：

1、处理NLP请求。

2、播放音乐和tts

3、控制音量。

4、控制网络状态。

5、提供app开发的基础sdk。

对下依赖shadownode。

对这个仓库，直接npm run test就可以。

看看package.json里怎么写的。

```
tools/test --reporter tap-nyan
```

test是一个shell脚本。

单元测试用例也写得比较全。



/usr/yoda/lib/app-runtime.js

这个怎么被使用的？

这里：

```
/usr/yoda/services/vuid/index.js:14:var AppRuntime = require('../../lib/app-runtime')
```

vuid的这里启动的。

```
/etc/init.d/vui-daemon:10:    procd_set_param command $PROG /usr/yoda/services/vuid/index.js
```

runtime这样启动的

```
    var runtime = new AppRuntime()
    runtime.init()
```

runtime里引用了这个配置

```
var ComponentConfig = require('/etc/yoda/component-config.json')
```

这个json文件里是这样：

```
{
  "paths": ["/usr/yoda/lib/component"],
  "interception": {
    "runtimeDidLogin": [ "ota.runtimeDidLogin" ],
    "turenDidWakeUp": ["custodian.turenDidWakeUp", "ota.turenDidWakeUp"]
  }
}
```

/usr/yoda/lib/component目录下有：

```
.
├── app-loader.js
├── app-scheduler.js
├── custodian.js
├── custom-config.js
├── dbus-registry.js
├── dispatcher.js
├── dnd-mode.js
├── flora.js
├── keyboard.js
├── lifetime.js
├── light.js
├── ota.js
├── permission.js
├── sound.js
├── turen.js
└── wormhole.js
```

会依次把这些component load进来

```
  ComponentConfig.paths.forEach(it => {
    this.componentLoader.load(it)
  })
```

loader的实现是：

```
var Loader = require('@yoda/bolero').Loader
```

loader具体做了什么？

就是创建这些class。

runtime的init函数回依次调用component的init函数。

```
AppRuntime.prototype.init = function init () {
  if (this.inited) {
    return Promise.resolve()
  }
  this.componentsInvoke('init')
```

### 在电脑上运行jsruntime

下载这个代码。里面tools下面有个build-yodart.sh的脚本。运行一下看看。

https://github.com/yodaos-project/yoda.js

出错了。需要看一下这个脚本。自己一步步地手动编译。

在目录下创建vendor目录。

然后下载node-flora的仓库，执行npm install的方式进行编译。

看看npm install做了什么。

调用了：

```
script/install && script/build
```

script/install的内容：

需要拉取下面这几个仓库。实际是拉取不到的。但是我在完整的yodaos的代码repo sync到的代码是有这个的。

我直接拷贝过来就行。

```
script/pull-deps --repo Rokid/aife-mutils --dest deps/mutils --ref master
script/pull-deps --repo Rokid/aife-cmake-modules --dest deps/cmake-modules --ref master
script/pull-deps --repo yodaos-project/flora --dest deps/flora --ref master

if test $test_build = "YES"; then
  script/pull-deps --repo yodaos-project/flora-dispatcher --dest deps/flora-dispatcher --ref master
fi
```

然后是要build这4个包。

参数要配置，因为我没有root权限，不能安装到系统目录下。

看了一下脚本内容，其实install目录也就是在out下面。所以可以通过脚本进行编译。

但是他最后有一句这个：

```
cp -r out/usr/* /usr
```

这就有点尴尬了。

我也不想在整理环境问题上花太多时间。

我反正有一台linux笔记本，上面安装好了一个Ubuntu 1604的docker环境，可以随意折腾，就把这个编译弄到那里面去做吧。

先执行./install-shadow-node.sh 命令。有点问题，改一下脚本就行。

现在编译shadownode出错。

```
libdbus-1.so.3: cannot open shared object file: No such file or directory
```

安装一下dbus就好了。

```
apt-get install dbus
```



# getprop

这个命令是Android的。

但是我看rokidos里也有。怎么实现的？

搜索一下：

```
./property_service/tools/getprop
```

对应这个：

```
./3rd/android_lib/bionic/property_service
./openwrt/package/rokid/property_service
```

系统里存在的prop文件有：

```
./default.prop
./system/build.prop
```



```
var DEFAULT_ALARM_RING = 'system://alarm_default_ringtone.mp3'
var DEFAULT_REMINDER_RING = 'system://reminder_default.mp3'
```

这样的路径，实际是在：

```
./opt/media/alarm_default_ringtone.mp3
```



参考资料

1、

https://blog.csdn.net/Carol_Luobo/article/details/109674413

# 知识点学习

我目前感觉到的：

config脚本的编写。我觉得没有必要。只要作为package放入到openwrt或者buildroot里就方便了。可能是为了对Android和服务器也通用吧。

cmake的大量使用。

自己实现的ipc通信机制flora。

# activity的概念

frameworks\jsruntime\apps\battery\app.js

以这个为例来看。

```
module.exports = function (activity) {
  var STRING_NOBATTERY = '当前产品没有电池，使用期间请连接电源'

  function speakAndExit (text) {
    return activity.tts.speak(text).then(() => {
      activity.exit()
    })
  }

  activity.on('request', function (nlp, action) {
    speakAndExit(STRING_NOBATTERY)
  })
}
```

这个activity怎么理解？

整个框架是怎样的？可以处理哪些消息？

frameworks\jsruntime\apps这个目录下的子目录，都有类似的结构。入口都是app.js。有package.json文件。里面配置权限等信息。

app.js的结构都是一个以activity为参数的函数。

函数里都是处理各种activity的消息。

/etc/yoda/app-loader-config.json

这个文件里：

```
{
  "paths": [
    "/opt/apps"
  ],
  "lightAppIds": [
    "@yoda/battery",
    "@yoda/composition-de-voix",
    "@yoda/custom-config",
    "@yoda/guidance",
    "@yoda/ota",
    "@yoda/system",
    "@yoda/volume",
    "@yoda/log-switch"
  ],
  "dbusAppIds": [],
  "cloudStackExcludedSkillIds": [
    "RB0BF7E9D7F84B2BB4A1C2990A1EF8F5",
    "ROKID.INTENT.WELCOME",
    "ROKID.INTENT.EXIT",
    "ROKID.EXCEPTION.CLOUD",
    "ROKID.EXCEPTION.NLP",
    "ROKID.EXCEPTION",
    "ROKID.CONFIRM",
    "ROKID.INTENT.CONFIRM_RETRY",
    "REQUEST_ERROR",
    "NO_NLP"
  ]
}
```

frameworks\jsruntime\runtime\lib\descriptor\activity-descriptor.js

这个文件就描述了activity相关的东西。

https://github.com/yodaos-project/yoda-book/blob/master/zh-cn/yodaos-source/02-glossary.md



## descriptor

frameworks\jsruntime\runtime\lib\descriptor\

这些也都有类似的结构。

```
1、继承了EventEmitter
2、
```

总共有这些：

```
module.exports = {
  ActivityDescriptor: require('./activity-descriptor'),
  ActivityTestDescriptor: require('./activity-test-descriptor'),
  HttpgwDescriptor: require('./httpgw-descriptor'),
  KeyboardDescriptor: require('./keyboard-descriptor'),
  LightDescriptor: require('./light-descriptor'),
  MultimediaDescriptor: require('./multimedia-descriptor'),
  TtsDescriptor: require('./tts-descriptor'),
  TurenDescriptor: require('./turen-descriptor'),
  WormholeDescriptor: require('./wormhole-descriptor')
}

```



作用是什么？

有必要弄清楚。这个概念设计全局的理解。

descriptor，顾名思义，就是描述。描述这些核心的概念的组成。

把类的prototype重写成返回json字符串的方式。这样就可以描述出类的构成。

那只是用来看的吗？怎么被其他代码实用呢？

在light-app.js里，就有这样的语句：

```js
  var descriptor = new ActivityDescriptor(appId, target, runtime)
  logger.log('descriptor created.')
  var activity = translate(descriptor)
  logger.log('descriptor translated.')
  descriptor.activity = activity
```

新建一个descriptor，然后用translate函数把它转成一个activity。

translate函数是怎么做的呢？

```JS
function translate (descriptor) {
  var activity = PropertyDescriptions.namespace(null, descriptor, null, null)
  return activity
}
```

从函数内容看，那就是通过descriptor构造出一个activity的意思吧。

从descriptor的注释里，可以看出，descriptor描述了通过flora发送的内容。

发送的类型有event、method。





appHome的概念又是什么？

是对应的app的目录位置的意思。

从这里可以看出来。

```
module.exports = function createLightApp (appId, metadata, runtime) {
  var target = _.get(metadata, 'appHome')
  logger.log(`load target: ${target}/package.json`)
```

这样调用到每个activity的处理函数的。

```
    logger.log(`load main: ${main}`)
    var handle = require(main)
    handle(activity)
```



# lightapp和extapp

我之前一直以为lightapp是灯光处理。

后面才意识到是轻量级的意思。

app的种类有这些：

```
/**
 *
 * @param {string} appId
 * @returns {'ext' | 'light' | 'dbus'}
 */
AppChargeur.prototype.getTypeOfApp = function getTypeOfApp (appId) {
  if (this.config.lightAppIds.indexOf(appId) >= 0) {
    return 'light'
  }
  if (this.config.dbusAppIds.indexOf(appId) >= 0) {
    return 'dbus'
  }
  if (_.get(this.getAppManifest(appId), 'rawExecutable', false) === true) {
    return 'exe'
  }
  return 'ext'
}
```



这篇文章提到了lightapp的设计理念。

https://zhuanlan.zhihu.com/p/60171122



YodaOS 作为一个前端操作系统，同样使用了类似的技术。

YodaOS 中的应用分为：lightapp 和 extapp，

前者是集成在语音交互运行时（Vui-daemon）进程内部的轻应用，

它主要是用于一个交互简单，需要快速响应的场景，

比如音量控制、系统控制等。

**后者作为一个独立的进程，通过 Child Process 与主进程通讯，**

使用场景主要是音乐、游戏、电话等需要**长时期使用的应用**。



**为什么要有轻应用？**

轻应用更像是一个脚本，

每当用户一次进行一次交互，

只需要从**预先加载**的脚本中调用定义在对应脚本的函数即可完成一次响应，

往往这类应用交互比较简单，

如果为此要创建在每次交互的过程中进行一次 ipc 甚至 fork 时，

无论对性能还是内存来说，都是比较浪费的。



在设计之初，我们期望对于开发者来说，并不需要针对不同类型的应用，

只需要在 package.json 中修改类型即可，

YodaOS API 应当保持完全一致。

这样的话，我们则面对一个问题，即使是能做到高度抽象，也需要在每次新增一个接口时，修改两处代码，这其实是有违我们的设计初衷的。

## 引入descriptor概念

为此，我们引入了 API Descriptor 的概念。

可以把它看作是用 JavaScript 写的 DSL，

**它用于描述每个 YodaOS API，**

包括命名空间、事件、方法等定义。

系统在初始化时，会加载所有 API Descriptor，**然后分别在 lightapp 和 extapp 生成对应的 API。**

```
Object.assign(ActivityDescriptor.prototype,
  {
    /**
     * When the app is active.
     * @event yodaRT.activity.Activity#active
     */
    active: {
      type: 'event'
    },
    /**
     * When the Activity API is ready.
     * @event yodaRT.activity.Activity#ready
     */
    ready: {
      type: 'event'
    },
    /**
     * When an activity is created.
     * @event yodaRT.activity.Activity#create
     */
    created: {
      type: 'event'
    }
  }
)
```

这样除了 API 定义可以统一起来了，也能比较方便地**基于 JSDoc 生成统一的 API Reference** 给开发者，使得整个 API 的修改能做到简单易读、门槛低和修改成本低等。

那么在 YodaOS 中，又是如何将上述的 Descriptor 生成为开发者直接使用的接口的呢？下面就为大家介绍我们引入的 Translator。

Translator也分为两种：

1、进程内的。translator-in-process.js

2、进程间的。translator-ipcjs



每个 translator 提供一个函数，即 translate(descriptor)。

它接受一个 descriptor 对象，

然后会遍历原型链中的对象，

并且分别按照 namespace、event 和 method 去**生成一个叫 activity 的对象**，

最后将这个对象返回给开发者。



light-app.js内部处理也非常简单，就几行关键代码。

关键就是通过descriptor生成activity，然后调用app/battery/app.js的处理函数就ok了。

ext-app.js的内部，则使用了这样的方式：关键就是fork了一个新的进程。

```
  var cp = childProcess.fork(entry, [ target, mode ], {
    cwd: target,
    env: Object.assign({}, process.env),
    stdio: 'inherit'
  })
```

ext-app的，就会考虑15s未响应的。

```
  return new Promise((resolve, reject) => {
    var timer = setTimeout(() => {
      cp.removeListener('message', onMessage)
      cp.kill()
      cleanup()
      reject(new Error(` ExtApp '${target}'(${cp.pid}) failed to be ready in 15s.`))
    }, 15 * 1000)

```



# speech-service

frameworks\allspark\speech-service

代码倒是不多。

这个用途是什么？

启动一个daemon程序，靠rpc来调用。



# 最佳实践

https://github.com/yodaos-project/yoda-book/blob/master/zh-cn/best-practice/01-testing.md

有效的测试是保证质量的基础。

通过快速有效的方法对应用进行测试，

是迭代开发应用中必不可少的工作流程。

编写第一个单元测试

假设你的应用的awesome-app。目录结构是这样：

```
-- ~/awesome-app
   |- package.json
   |
   |- /test
   |  |- cool-func.test.js
   |
   |- /src
   |  |- app.js
   |  |- cool-func.js
```

在cool-func.js里，内容是这样：

```
module.exports = function coolFunc() {
	return "happy testing"
}
```

那么在cool-func.test.js里，编写测试用例如下：

```
var test = require('@yodaos/mm').test
var coolFunc = require('../src/cool-func')

test('happy testing', t=> {
	t.strictEqual(coolFunc(), 'happy testing')
	t.end()
})
```

运行单元测试

先用yoda-cli命令把应用代码和test安装到设备。

```
yoda-cli pm install .
```

然后通过instrument模式启动应用，同时监听应用的输出。

```
yoda-cli am instrument awesome-app 'test/*.test.js'
yoda-cli am logread awesome-app
```

# 稳定性

yodaos开发应用的时候，需要关注应用的性能和稳定性。

包括：

* 快速启动
* 快速语音交互。
* 不出现异常与崩溃。

## 启动

当一个应用被启动后，yodaos希望应用在5s内完成启动的逻辑。

如果5s内没有启动完成，应用会被kill掉。

如果应用内部有阻塞操作，那么应该去掉阻塞逻辑。

## 进程和线程

yodaos会为每个应用场景一个单独的进程。

应用的代码将会在Jerryscript主线程执行。

应用的主线程，主要负责接收并处理系统事件（NLP、按键等）。

因此主线程一般也叫UI线程。

由于主线程的特殊性，不要阻塞主线程，会导致应用失去响应。

同时，因为iotjs不是线程安全的编程的模型。

不要在其他的线程里操作iotjs的相关api。

阻塞的改成异步回调的方式。



在yodaos里，建议优先使用libtuv的线程池来处理多线程逻辑。

使用N-API和libtuv进行多线程处理。

如果有计算密集的操作，建议通过N-API放到c代码里实现。



## ANR

ANR是应用未响应的缩写。

当应用的主线程因为某种原因被长时间阻塞时，app会出现ANR。

这个行为对app是透明的，是runtime负责的。

yodaos使用下面的规则来判断和处理ANR：

1、app底层会每5秒给yodaos发送一个心跳。

2、当yodaos连续3个间隔（也就是15s）没有收到应用的心跳时，就会发信号重启App。

可能导致ANR 的原因有：

* 在主线程做同步io操作。
* 在主线程做长时间的密集计算。
* 主线程等待其他线程完成。
* 主线程被死锁。

常用的解决方法：

* 对于大量密集计算的情况，yodaos系统提供了一个simpleperf等工具查看一段时间内应用里的函数的调用情况（需要库没有被strip过），如果cpu大部分时间消耗在虚拟机内，可以通过shadownode的CPU profiler工具生成火焰图来查看脚本的函数调用情况。
* 对于同步io、线程同步、死锁等情况，使用strace来查看系统调用情况。

5s的定时是这里做的。

frameworks\jsruntime\runtime\client\ext-helper.js



## 内存管理

无论在什么样的环境中开发应用，内存都是要时刻关注的点。

yodaos的应用的内存是jerryscript虚拟机在管理。

虚拟机通过ref count、flag clear算法来执行gc。

在虚拟机heap小于某个值的时候，会触发gc。

从而保证内存可用。

但是开发者还是要在某些场景关注内存的情况。

下面是几种场景的内存泄漏：

1、对象被全局或者闭包变量引用导致无法释放。

```
var obj = {}
setInterval(() => {
  var timestamp = Date.now()
  obj[timestamp] = true
}, 1000)
```

2、使用N-API场景或者获取对象后，没有释放。

本质是C语言里泄漏了。

3、多线程回调没有开启Handle Scope。

开发者可以通过process.memoryUsage()来获取进程的常驻内存大小rss、虚拟机的内存池大小heapTotal以及虚拟机内存池的使用大小heapUsed。

当进程出现内存泄漏时，可以定时打印heapUsed。

这个时候，可以用shadownode提供的heap profiler工具来生成多次虚拟机内存的snapshot。通过比较snapshot来确定哪些对象在泄漏。

## 异常处理

当脚本出现未捕获的异常时，shadownode会将这个异常抛到全局对象process对象中。

如果这个时候，你没有监听process对象的异常，那么shadownode就会强制退出应用。

# 开发手册

## 建立你的第一个App

### yodaos开发者工具

工具目录在这里：

https://github.com/yodaos-project/yoda-platform-tools

工具包括了：

1、yoda-cli。命令行工具，跟yodaos device进行交互。

2、yoda-platform-lib。一个库，让你可以写代码同时跟多个yodaos设备进行交互。

3、yoda-vscode。vscode插件。

### 创建yodaos应用

```
yoda-cli init app awesome-demo-app
```

安装到设备

```
yoda-cli pm install awesome-demo-app
```

### 程序入口

对于yodaos来说，每一个app都是一个commonjs模块。

app的主入口是通过

```
var Application = require('@yodaos/application').Application
var app = Application()
```

而创建的Application实例。

应用通过这个app对象来与runtime交互，接收事件等。

### 接收系统事件

在创建Application的时候，参数是一个字面对象。

这个对象可以挂载多个事件的监听函数，通过这些监听函数来监听系统和应用的event。

```
var app = Application({
	url: function url(urlObj) {
		
	},
	broadcast: function broadcast(event) {
	
	}
})
```

### 应用的manifest文件

除了程序代码，app还需要向系统表明自己的身份、权限请求等信息。

以便想系统申请资源。

yodaos应用的package.json就包括了这些信息。

package.json的大部分字段跟npm的package.json差不多。但是了都几个重要的字段。

name和manifest。

name向系统表明了自己的身份。

manifest则表明了自己要申请的资源。

```
{
	"name": "com.xx.yy.awesome-app",
	"version: "1.0.0",
	"main": "app.js",
	"manifest": {
		"services": [
			["a-service", {"main": "a.js"}],
			"b-service"
		],
		"hosts": [
			"awesome-app"
		]
	}
}
```

### 处理url请求

应用可以通过url的方式启动其他的应用。

如果希望处理某个url，那么需要在package.json里注册这个rul。

例如：

```
{
  "name": "com.example.app.foobar",
  "manifest": {
    "hosts": [
      "foobar.app"
    ]
  }
}
```

现在这个应用就可以处理这一个请求：

```
yoda-app://foorbar.app/data/media/music.mp3
```

具体处理如下：

```js
var Application = require('@yodaos/application').Application
var AudioFocus = require('@yodaos/application').AudioFocus
var MediaPlayer = require('@yoda/multimedia').MediaPlayer
var logger = require('logger')('app')
var path = require('path')

var app = Application({
    url: function url(urlObj) {
        logger.info('received url:', urlObj.href);
        var focus = new AudioFocus()
        var resumeOnGain = false;
        var player
        //执行播放处理
    }
})
```

## AudioFocus

这个话题比较独立，跟总体架构关系不大。我暂时不关注。

https://github.com/yodaos-project/yoda-book/blob/master/zh-cn/guidance/02-audio-focus.md

## Lightd

灯光处理。这个可以先看看。因为架构设计设计非常多，可以先看看，从中窥探整个架构设计的风格。

yodaos使用lightd来管理灯光。

所有的灯光显示，都交给这个进程去处理。

这是基于下面的考虑：

* 方便开发者编写复杂的灯光效果。lightd提供抽象的effects灯光效果库。开发者使用effects库很容易组合各种小狗，并按顺序执行它。
* 资源管理。
* js是异步的。
* 模块化。
* 灯效被打断后的恢复机制。
* 优先级机制。



# yoda-rt.d.ts

这个typescript定义文件。可以看出重要的类的结构。

```
namespace YodaRT {
	class Activity extends EventEmitter {
		light: LightClient
		media: MediaClient
		tts: TtsClient
		appId: string
		appHome: string
		
		//这些方法都是返回Promise的。
		exit()
		get(key:string)
		playSound(uri:string)
		setComfirm()
		setPickup()
		setBackground()
		setForgournd()
		//event
		on(event: 'ready', listener: ()=>void): this
		'create'
		'pause'
		'resume'
		'destroy'
		'request'
		
		class LightClient {
			play()
			stop()
		}
		class MediaClient {
			getLoopMode()
			getPosition()
			pause()
			resume()
			seek()
			setLoopMode()
			start()
			stop()
		}
		class TtsClient() {
			speak()
			stop()
		}
		interface Request() {
			appId
			intent
			slots: {
				[key:string]: {
					type: string
					value: string
				}
			}
		}
	}
}
```

# 开机流程分析

入口是openwrt\build_dir\target-aarch64_cortex-a53_glibc-2.22\root-brcm2708\usr\yoda\services\vuid\index.js

```
var AppRuntime = require('../../lib/app-runtime')

 var runtime = new AppRuntime()
    runtime.init()
```



```
inherits(AppRuntime, EventEmitter)
```

init函数的过程

```
1、this.componentsInvoke('init')
	把所有注册的Component依次调用对应init函数。
	Component在AppRuntime的构造函数里进行注册并load的。
	  this.componentLoader = new Loader(this, 'component')
      ComponentConfig.paths.forEach(it => {
        this.componentLoader.load(it)
      })
```



看Load的构造函数

```
需要2个参数
	1、runtime。
	2、property。
	
```



越看还是越觉得这套方案对于智能音箱场景还是太复杂了。

这套方案第三方很难玩得转。

本来C语言很容易就可以实现的功能，在这里绕了一大圈。

也许有较好的扩展性，但是带来的坏处远大于好处。



不过在第三方应用的支持这一点上还是不错的。

但是问题是一般很少有在板端做应用的吧。

都是在云端做应用。

思路值得学习。

# yoda-cli用法

使用 yoda-cli 发送文本指令

```
./yoda-cli flora call yodaos.voice-interface.nlp '["深圳天气"]' voice-interface
./yoda-cli flora call yodaos.voice-interface.nlp '["播放音乐"]' voice-interface
./yoda-cli flora call yodaos.voice-interface.nlp '["禁麦"]' voice-interface
./yoda-cli flora call yodaos.voice-interface.nlp '["拉肚子不能吃什么"]' voice-interface
./yoda-cli flora call yodaos.voice-interface.nlp '["音量50"]' voice-interface
```

用yoda-cli创建的app目录是这样：

```
~/work/test/yoda-cli-test$ tree
.
├── demo-app
│   ├── app.js
│   └── package.json
└── yoda-cli
```

app.js的内容是：

```
module.exports = function main (app) {
  app.on('request', nlp => {
    app.tts.speak('Hello from ')
  })
}
```

app和activity是一个东西。

参考资料

1、

https://www.sodocs.net/doc/1511227930.html

# js runtime如何执行对应的app

例如，调节音量，怎么调用到frameworks\jsruntime\apps\volume\app.js

应该是靠接收消息。

```
  activity.on('request', handleWrap(function (nlp, action) {
    var partition = 10
    var vol
    switch (nlp.intent) {
      case 'showvolume':
```

每个js文件都是一个独立的iotjs进程吗？

LaVieEnPile.prototype.activateAppById 这个函数做了什么？

这个接口已经过时了。

```
Deprecated: Use AppScheduler.createApp instead.
```

都是在app-runtime.js里进行createApp的。

例如这里startDaemonApps

在`AppRuntime.prototype.onLoggedIn`的时候，会调用很多的app创建。

# js runtime services 

代码在这里

frameworks\jsruntime\runtime\services

有几个：

```
activation
	这个是纯c++代码，在开机时启动。
	作用是：
	Client::connect("unix:/var/run/flora.sock"
	
lightd
multimediad
otad
	ota后台服务。
	把js封装到shell脚本里，然后开机调用。
	
ttsd
	tts后台服务。
vuid
	这个是runtime的主要服务。靠这里来拉起其他的App。
```

# 交互流程

下面简单介绍一下语音交互的流程，如下：

1. 用户的语音在云端解析完后**通过 MQTT 服务推送相应的 NLP 数据到 VUI**
2. VUI 服务**选择对应的本地应用**处理数据
3. 如果应用的处理中包含灯光、播报等逻辑，会通过 VUI 来调用对应的服务来执行逻辑



参考资料

https://yodaos-project.github.io/yoda-book/zh-cn/yodaos-source/00-source-tree.html

# 按键行为定制

这个确实支持功能很丰富。



https://yodaos-project.github.io/yoda-book/zh-cn/yodaos-source/customization/01-keyboard.html

# 灯效定制

这个设计思路值得学习。

代码放在这里。使用了标准的Android的 HAL架构。



hardware\modules\leds

https://yodaos-project.github.io/yoda-book/zh-cn/yodaos-source/customization/02-light.html



# 作者的一些回复

YodaOS 以另外的方式去做 AR 了，Node.js 操作系统的话还是要再继续加油，不过可以看看鸿蒙 OS 的 JS 应用框架哦

https://zhuanlan.zhihu.com/p/55959617

知乎专栏

https://www.zhihu.com/column/yodaos



最中间的是以 Linux 为主的 128+128 组合的设备，最为我们所熟知的就是智能音箱（无屏），对于这类设备来说包括 Alexa、Rokid、小爱同学等，**现在大多数厂商在设备端的开发语言也都以 C + Lua 为主**，目前也仅有 Rokid 支持 JavaScript 直接运行在设备端，而本文也主要是针对智能音箱这一挡设备来展开。



## string对象创建太多问题的优化

**就是要尽量使用字符串模板，而不要使用字符串拼接的方式。**

这件事其实发生在一个月前，我们设备端的代码刚刚移植到一款单核 CPU 的低端设备中，意外发现运行非常缓慢，当时并没有相对比较完整的 CPU Profiling 工具，只能通过日志的方式，发现在虚拟机内部存在大量的 String 对象创建，是其他对象的600倍左右。

这时，我们就去查找引擎内部的代码，慢慢定位到了 util#format 这个函数上，它内部会把大量字符串、数字、对象等都创建一个新的 String，并且还存在着递归和 while 循环，因此我想到的第一件事就是通过 String Template 来替代字符串拼接，并且针对单个参数的调用做优化，把第一个参数直接输出到 Stdio，避免了大量调用 util#format 的情况。

通过这个改动，我们把之前的 String 对象数量下降到了跟其他种类持平，同时建议上层的应用开发者使用 String Template 来替代 console.log 的多参数调用，这样整个业务代码最终的性能提升了20%。

# 树莓派搭建yodaos的环境

前面我已经通过repo的openwrt，手动编译出镜像了。

现在烧录也可以跑起来。

但是串口不知道为什么打印不了。

我接的hdmi显示屏。

默认没有带ssh服务端，也没有adbd的程序。

我是不是要编译一个才好呢？

yoda-cli安装程序，是走的什么通路呢？

从yoda-cli依赖的yoda-platform-lib来看。

里面依赖了adb，那就是走adb的了。

那就看能不能走网络的adb。因为我的电源线就是一根。也许可以同时从电脑供电看看。

进来看看网络的方式行不行。

算了。感觉搭建环境还是要不少时间，先不做了。

yoda-cli是适合安装在macos或者linux下的，因为用到了bash。

看release包，也只有linux和macos的。

# yodaos语音交互过程

以下章节涉及到的知识点包括（可以先自行查阅之）：

- 语音激活（VT）
- 语音识别（ASR）
- 语义理解（NLP）
- 语音合成（TTS）
- 技能（Skill）——语音交互时代的应用

云端是怎么把有单文本解析成json格式的呢？

这就要引入领域domain的概念。

例如

“今天的天气”会被划入到天气领域。

“我要开灯”是iot领域。

“我要听歌”是音乐领域

可以理解领域为一个大概的范围。

表示当前用户要跟设备交流的主题。

然后有意图的概念。

意图是在领域之下的。

例如：“今天的天气”，领域是天气，而意图则是查询。

有了领域的概念后，我们获取到一串文本后，会把文本交给一个AI模型，模型判断出文本命中的领域和意图。

然后从文本中抽取其他的信息。

组合成一个json字符串下发给设备端。



语音交互的输出比较单一，

主要就是：tts、音效、音乐。

这里有一个VUI renderring的概念。

在GUI时代，渲染的输出是屏幕的控件、声音和视频。

VUI就是TTS、音效和音乐。

跟web一样，VUI也可以分为服务端渲染和本地渲染。



本地渲染

> 本地直接处理NLP数据，在本地执行业务逻辑。

服务端渲染

> 服务端处理完逻辑，把最终结果给本地执行。

在服务端渲染的应用，称为CloudApp。



技能的生命周期

无论是本地还是云端，技能跟网页一样，也有自己的生命周期。

VUI runtime会对他们进行管理。

在yodaos里，每个技能有两种启动方式：

1、NLP下发命令启动。

2、按键等设备方式启动。

每个技能在启动后，会处于技能栈的栈顶。

表示当前的技能正在运行。

技能这时候可以控制设备的输出。

与此同时，如果之前有技能已经在运行，会先把该技能销毁或者暂停。

具体是销毁还是暂停，取决于之前这个技能是即时技能还是场景技能。

即时技能

> CUT。用于单次会话的技能，当前有新的技能命中时，毫不犹豫地销毁这个技能。

场景技能

> SCENE。用于长时间需要交互的技能，例如音乐播放。如果新的技能是CUT，那么在CUT后，会恢复之前的技能，如果新的技能也是SCENE，那么就替换之前的技能。



如果是做产品，不用做这么多抽象。

但是要做平台，必须要解决不同平台的重复工作。这就必须要借助抽象。

没有必要移植到buildroot。



如果用纯C语言来复刻这套逻辑。

应该怎么做呢？

其实可以都在一个进程内搞定吧。

重点还是考虑一下第三方扩展怎么放进来，以及标准化api提供便利性。



# js里调用shell脚本

jsruntime\runtime\lib\cloudapi

这个里面就是用js调用了shell脚本，看看怎么处理返回结果的。

就是在回调里处理的。



# ppt资料

这里有一些分析的ppt。

https://github.com/NodeParty-China/Node-Party/

# tts是怎么播放出来的

tts应该是离线的，是直接播放文件，还是用什么库合成的？

jsruntime\runtime\lib\descriptor\tts-descriptor.js

函数在这里实现。

本质是通过dbus去调用的。

# 工厂测试

这套代码还是很齐全的。还包含了工厂测试相关的文档和代码。

而且测试做得很专业。不只是简单看硬件的好坏。代码里参考的连接也给了。可以了解不少相关的知识。

值得消化吸收一下。

# 单独把js runtime跑起来

最有价值的也就是这部分了。

我可以考虑自己把这部分跑起来做一些测试。

也做一个基本的iotjs验证环境。

能不能直接在Linux跑？

如果有root限制，可以考虑在qemu里跑。

```
iotjs ./node_modules/tape/bin/tape.js 
```

必须要qemu环境。

因为测试脚本里很多的东西都是基于绝对路径的。

或者弄一套基于openwrt的qemu环境。

# 写一个应用framework，方便上层进行应用开发，就像android应用开发基于Activity一样

编写一个类似 Android 应用开发中基于 Activity 的应用框架，可以通过以下步骤实现：

1. **定义基本的应用程序类（Application）**：这个类可以是整个应用程序的入口点，负责初始化应用程序的全局状态和设置。您可以在这个类中提供一些全局方法和属性，以方便其他部分的访问。

2. **定义界面元素（UI Elements）**：类似于 Android 的 Activity，您需要定义一些界面元素来展示应用程序的用户界面。这些界面元素可以是窗口、面板、控件等。

3. **定义应用程序状态管理**：您可能需要实现类似于 Android 的生命周期管理，以便在应用程序启动、暂停、恢复和销毁时执行相应的操作。

4. **处理用户输入和事件**：您需要编写代码来处理用户的输入和应用程序中发生的事件。这可能涉及到监听器、回调函数等。

5. **定义应用程序导航**：如果应用程序有多个界面或模块，您可能需要实现一种导航机制，以方便用户在不同的界面之间切换。

6. **提供数据持久化和通信功能**：您可能需要提供一些数据持久化和通信功能，以便应用程序能够保存数据到本地或与服务器进行交互。

7. **提供扩展机制**：为了方便上层应用开发人员扩展应用程序的功能，您可以提供一些扩展机制，例如插件系统、模块化设计等。

8. **编写文档和示例代码**：为了让其他开发人员能够轻松使用您的应用框架，您需要编写清晰的文档和示例代码，以说明如何使用框架的各种功能。

在实现以上步骤时，您可以选择使用编程语言和技术栈，例如使用 Python 和 PyQt、使用 Java 和 JavaFX、使用 C# 和 Xamarin 等。根据您的项目需求和技术背景，选择适合您的工具和技术进行开发。

## 用nodejs来写一个这样的应用框架示例，有没有现成的开源代码？或者你给我一个最小的参考实现

在 Node.js 中编写一个类似于 Android 应用开发中基于 Activity 的应用框架是完全可能的。

虽然没有像 Android 那样通用的标准框架，

但您可以使用 Node.js 的模块化和事件驱动的特性来创建自己的框架。

以下是一个简单的示例，演示了如何在 Node.js 中实现一个基本的应用框架：

```javascript
// app.js

// 导入所需模块
const EventEmitter = require('events');
const readline = require('readline');

// 创建一个应用程序类
class Application extends EventEmitter {
  constructor() {
    super();
    // 初始化应用程序状态
    this.state = 'idle';
    // 创建界面管理器
    this.screenManager = new ScreenManager();
  }

  // 启动应用程序
  start() {
    this.emit('start');
    this.screenManager.render(); // 渲染初始界面
    this.handleUserInput(); // 处理用户输入
  }

  // 处理用户输入
  handleUserInput() {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    rl.on('line', (input) => {
      this.emit('input', input.trim());
    });
  }
}

// 创建一个界面管理器类
class ScreenManager {
  // 渲染界面
  render() {
    console.log('Welcome to my application!');
    console.log('Please enter your command:');
  }
}

// 实例化应用程序
const app = new Application();

// 监听应用程序启动事件
app.on('start', () => {
  console.log('Application started.');
});

// 监听用户输入事件
app.on('input', (input) => {
  console.log('User input:', input);
  // 在这里可以根据用户输入执行相应的操作
});

// 启动应用程序
app.start();
```

这个示例中，我们创建了一个简单的应用框架。应用程序类 `Application` 包含了应用的核心逻辑，它继承了 Node.js 的事件发射器类以处理事件。界面管理器类 `ScreenManager` 负责渲染应用的界面。应用程序在启动时渲染初始界面，并监听用户的输入事件。

当用户输入时，应用程序会触发 `input` 事件，并将用户输入作为参数传递给事件处理函数。您可以在事件处理函数中根据用户输入执行相应的操作，例如切换界面、处理命令等。

请注意，这只是一个简单的示例，用于演示如何在 Node.js 中实现一个基本的应用框架。实际的应用框架可能需要更复杂的逻辑和功能，例如路由管理、状态管理、数据持久化等。您可以根据您的项目需求和复杂程度进行扩展和定制。

## 要可以设计这样一个完整的应用框架，我应该阅读哪些书籍和代码来提高自己的设计和代码能力

设计和编写一个完整的应用框架需要综合运用多方面的知识和技能。以下是一些书籍和资源，可以帮助您提高设计和编码能力，以及理解应用框架的设计原则和最佳实践：

1. **软件架构模式**：
   - 《软件架构设计的艺术》（The Art of Software Architecture）：该书介绍了软件架构设计的基本概念、设计原则和常见架构模式，对于理解和设计应用框架非常有帮助。
   - 《模式语言：建筑、城镇、程序》（A Pattern Language: Towns, Buildings, Construction）：虽然这本书主要关注建筑领域的模式语言，但其中的许多概念和原则也适用于软件架构设计。

2. **设计模式**：
   - 《设计模式：可复用面向对象软件的基础》（Design Patterns: Elements of Reusable Object-Oriented Software）：这是设计模式领域的经典之作，介绍了常见的软件设计模式，包括工厂模式、单例模式、观察者模式等。掌握这些设计模式可以帮助您更好地设计和组织应用框架的代码结构。

3. **Node.js 相关书籍**：
   - 《深入浅出 Node.js》（Node.js in Action）：该书介绍了 Node.js 的基本概念、核心模块和常用的开发技术，对于了解和使用 Node.js 来构建应用框架非常有帮助。
   - 《Node.js 设计模式》（Node.js Design Patterns）：这本书介绍了在 Node.js 中使用的各种设计模式和最佳实践，适合进阶学习者。

4. **项目实战和开源代码**：
   - 参与开源项目：选择一些流行的开源项目，并积极参与其开发过程，可以帮助您学习到实际项目开发中的设计和编码技巧。
   - 阅读优秀的开源项目代码：阅读一些优秀的开源项目代码，了解其设计思想、架构和实现方式，可以帮助您提高代码质量和设计能力。

5. **软件工程和系统设计**：
   - 《代码整洁之道》（Clean Code: A Handbook of Agile Software Craftsmanship）：这本书介绍了如何编写清晰、可读、可维护的代码，是每个软件工程师都应该阅读的经典之作。
   - 《系统架构设计师》（Becoming a Software Architect）：这本书探讨了成为一名优秀的软件架构师所需的技能、知识和经验，对于理解和设计应用框架的整体架构非常有帮助。

通过阅读上述书籍和资源，并结合实际的项目实践和开源代码学习，您将能够提高自己的设计和编码能力，设计并实现出更加健壮和灵活的应用框架。

# 板端目录分布

### Applications

The application has system and user types.

- `/opt/apps` for system application.
- `/data/apps` for userscope application.

### Resources

- `/opt/light` for system light resource.
- `/opt/media` for system media resource.

### Configurations

- `/etc/yoda` for configurations like keyboard, env, and more.



# shell脚本总结

这个里面涉及到不少的脚本。

感觉这些脚本的用法有值得学习参考的地方。

所以总结一下。

从最外层一层层往里面挖掘吧。

## build.sh

打印usage的方法：这个方法和格式都值得参考。

```
usage() {
cat <<USAGE

Usage:
    bash $0 -p <PRODUCT> -f <IMG_FOLDER> -n <IMG_NAME> -j 32 [OPTIONS]
    eg: ./build.sh -p leo_k18_universal_node -n openwrt-leo-k18-universal -f leo-k18-universal -r 

Description:
    Builds Openwrt for given PRODUCT

OPTIONS:
    -d, --debug
        Enable debugging - change Debug/release image

    -c, --clean
        Make distclean 

    -r, --remove
        Make clean

    -h, --help
        Display this help message

    -j, --jobs
        Specifies the number of jobs to run simultaneously (Default: 8)

    -p, --product
        The product name (openwrt/configs/<PRODUCT>_defconfig, eg: leo_k18_universal_node)
		
    -f, --folder
        Image folder (eg:leo-k18-universal)

    -n, --name
        Image name  (eg:openwrt-leo-k18-universal)

    -s, --solid file system, a113===>squashfs
		Read only filesystem

USAGE
}
```

选项的设置：

```
long_opts="debug,clean,folder:,help,jobs:,product:,name:,module:,solid_filesystem:"
getopt_cmd=$(getopt -o dcrf:hj:p:n:m:s: --long "$long_opts" \
            -n $(basename $0) -- "$@") || \
            { echo -e "\nERROR: Getopt failed. Extra args\n"; usage; exit 1;}
eval set -- "$getopt_cmd"
```



`eval set -- "$getopt_cmd"`：

这行代码将`getopt`命令的输出作为字符串传递给`eval`命令，

`set -- "$getopt_cmd"`将`$getopt_cmd`的内容设置为位置参数（即脚本的命令行参数）。

这样做的目的是重新设置脚本的位置参数，使得之后的代码可以直接通过`$1`、`$2`等访问到解析后的命令行参数。

逐个解析参数：

```
while true; do
    case "$1" in
        -d|--debug) DEBUG="true";;
        -c|--clean) CLEAN_OUTPUT_PRODUCT_DIR="true";;
        -m|--module) PACKAGES_TO_CLEAN=$(echo $2 | tr "," "\n");;
        -r|--remove) REMOVE_OUTPUT_PRODUCT_DIR="true";;
        -f|--folder) IMG_FOLDER="$2";;
        -h|--help) usage; exit 0;;
        -j|--jobs) JOBS="$2"; shift;;
        -p|--product) PRODUCT="$2"; shift;;
        -n|--name) IMG_NAME="$2"; shift;;
        -s|--solid_filesystem) BUILD_ROOT_FILESYSTEM="$2"; shift;;
        --) shift; break;;
    esac
    shift
done
```



# 参考资料

1、OpenWrt构建中遇到的问题以及解决办法

https://blog.csdn.net/qq_31952033/article/details/103527281

2、

这篇文章里很全面了。

https://blog.csdn.net/kuangzuxiaoN/article/details/121458746