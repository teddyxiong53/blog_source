---
title: yodaos（1）
date: 2022-08-09 19:15:08
tags:
	- yodaos

---

--

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



# speech-service

frameworks\allspark\speech-service

代码倒是不多。

这个用途是什么？

启动一个daemon程序，靠rpc来调用。





# 参考资料

1、OpenWrt构建中遇到的问题以及解决办法

https://blog.csdn.net/qq_31952033/article/details/103527281

2、

这篇文章里很全面了。

https://blog.csdn.net/kuangzuxiaoN/article/details/121458746