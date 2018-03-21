---
title: 《Android系统源代码情景分析》读书笔记
date: 2018-03-21 15:41:44
tags:
	- 读书笔记

---



目录

```
系统篇
1、准备
2、HAL层。
3、智能指针
驱动篇
4、logger
5、Binder
6、Ashmem
应用框架篇

```

书一共840页。



关于代码下载，打死我也不用repo的方式下载，上次下载了几天，最后各种错误，愣是不行。

https://pan.baidu.com/share/link?shareid=7577&uk=4246628909

这位兄弟是好人，下载了上传到网盘。我下载下来看看。用idm下载，很快。几分钟就搞定了。

是7z压缩的解压：

```
7za e Android_kernel.7z
```

解压后是一个tar文件，再解开。

打印了很多hard link不存在的问题。先不管，看看能不能编译。

hard link是因为用repo下载的。

解压后，是3.1G。下载的文件是500M。压缩比挺高的。

把.git目录都删掉，小了100M。

```
teddy@teddy-ubuntu:~/work/android/mydroid$ make help
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.5
TARGET_PRODUCT=generic
TARGET_BUILD_VARIANT=eng
TARGET_SIMULATOR=
TARGET_BUILD_TYPE=release
TARGET_BUILD_APPS=
TARGET_ARCH=arm
HOST_ARCH=x86
HOST_OS=linux
HOST_BUILD_TYPE=release
BUILD_ID=GINGERBREAD
============================================
/bin/bash: prebuilt/linux-x86/toolchain/arm-eabi-4.4.3/bin/arm-eabi-gcc: No such file or directory
/bin/bash: prebuilt/linux-x86/toolchain/arm-eabi-4.4.3/bin/arm-eabi-gcc: No such file or directory
/bin/bash: bison: command not found
Checking build tools versions...
************************************************************
You are attempting to build with the incorrect version
of java.
 
Your version is: openjdk version "1.8.0_151".
The correct version is: 1.6.
 
Please follow the machine setup instructions at
    http://source.android.com/download
************************************************************
build/core/main.mk:118: *** stop.  Stop.
```

提示了3个错误。

gcc工具链。哪里指定的？

bison我安装一下就好了。

我解决java版本的问题。

要1.6，我就安装1.6版本的。

```
build/core/prebuilt.mk:91: *** recipe commences before first target. Stop.
```

这里很纠结，就是空格和tab的问题。

这部分代码注释掉。先往下走。在build/core/prebuilt.mk里。

```
#ifneq ($(prebuilt_module_is_a_library),)
#ifneq ($(LOCAL_IS_HOST_MODULE),)
#	$(transform-host-ranlib-copy-hack)
#else
#	$(transform-ranlib-copy-hack)
#endif
#endif
```

```
/usr/include/features.h:367:25: fatal error: sys/cdefs.h: No such file or directory
```

这个用 sudo apt-get install libc6-dev-i386来解决。

然后继续。

```
/usr/include/c++/5/string:38:28: fatal error: bits/c++config.h: No such file or directory
```

安装这个。

```
sudo apt-get install g++-multilib
```

继续。

```
external/clearsilver/java-jni/../util/neo_err.h:88:69: error: expected expression before ‘)’ token
    nerr_raisef(__PRETTY_FUNCTION__,__FILE__,__LINE__,e,f,__VA_ARGS__)
```

https://stackoverflow.com/questions/42979203/c-macro-compilation-error-aosp-external-clearsilver-util-neo-err-h

看解释是因为展开后多了一个逗号。

改成：

```
nerr_raisef(__PRETTY_FUNCTION__,__FILE__,__LINE__,e,f,##__VA_ARGS__)
```

加了2个#号。

后面还有类似错误，一样解决。

还是有很多错误，我暂时不编译了。这个太耗时间。不是我当前关注的重点。



freg设备。就是fake register。只有一个寄存器，大小4个字节。可读可写。

看写法，跟linux的驱动写法是一样的。但是这里给的示例，写得比较全面。可以参考。

测试程序用的也是C写的。

然后是继续写freg的hal层代码。









