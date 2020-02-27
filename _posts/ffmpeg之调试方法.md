---
title: ffmpeg之调试方法
date: 2020-02-26 09:47:40
tags:
	- 视频

---

1

gdb调试方法

目前的问题是，我另外安装了ffmpeg，自动会去连接系统目录下的动态库。

而很多代码都是在动态库里的。

我当然是希望优先连接当前目录下编译出来的动态库。

或者简单点，让生成的ffmpeg，完全进行静态链接。

```
teddy@teddy-ThinkPad-SL410:~/work/ffmpeg-compile/ffmpeg-4.2.2$ ldd ./ffmpeg_g
        linux-vdso.so.1 =>  (0x00007ffd5acd6000)
        libavdevice.so.58 => /usr/local/ffmpeg/lib/libavdevice.so.58 (0x00007fcd76ee2000)
```

手动在Makefile里加-static选项，会链接不过。

用下面命令配置一下看看。

```
./configure --extra-ldexeflags="-static"
```

这样编译是好的。可以用来调试了。

直接用打印的方式来调试还方便点。

修改后，直接make，就可以把修改编译进来。

目前编译有优化，在单步执行的时候，跳转很没有规律。

在ffbuild/config.mak里，搜索"-O"，可以看到默认是O3 的，改成O0的。

再touch一下example的例子。make examples。这样就可以直接生效了。

但是如果改动了库里面的代码，则会编译所有的examples。也比较耗时。

可以在config.mak里，把不需要的example的配置项改成no。





参考资料 

1、

https://github.com/zimbatm/ffmpeg-static/blob/master/build.sh