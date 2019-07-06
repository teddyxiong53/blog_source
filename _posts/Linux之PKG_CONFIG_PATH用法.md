---
title: Linux之PKG_CONFIG_PATH用法
date: 2019-07-06 15:15:37
tags:
	- Linux
---



现在编译gstreamer，我先编译了gstreamer，安装在自定义的目录下，然后编译gstreamer base plugin。

结果还是试图从系统里去找gstreamer，这个当然是找不到的。

但是这样设置一下，就可以了。

```
export PKG_CONFIG_PATH=/home/teddy/tools/install/gstreamer/lib/pkgconfig:$PKG_CONFIG_PATH
```

PKG_CONFIG_PATH这个起了什么作用？



还有一个pkg-config命令。这个命令的作用又是什么？

pkg-config命令是用来查询已经安装的库的命令。

这个命令最初是在Linux上的，后面被移植到其他系统。

当安装一个库的时候，会包含一个后缀名为pc的文件。

这个pc文件会被放入到系统的某个目录下。

例如在Linux上，是你make install之后，lib目录下的pkgconfig目录下。

gstreamer的pc文件内容是这样的。

```
teddy@teddy-ThinkPad-SL410:~/tools/install/gstreamer/lib/pkgconfig$ cat gstreamer-1.0.pc 
prefix=/home/teddy/tools/install/gstreamer
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include/gstreamer-1.0
toolsdir=${exec_prefix}/bin
pluginsdir=${exec_prefix}/lib/gstreamer-1.0
datarootdir=${prefix}/share
datadir=${datarootdir}
girdir=${datadir}/gir-1.0
typelibdir=${libdir}/girepository-1.0

Name: GStreamer
Description: Streaming media framework
Version: 1.14.4
Requires: glib-2.0, gobject-2.0
Requires.private: gmodule-no-export-2.0 libunwind 
Libs: -L${libdir} -lgstreamer-1.0
Cflags: -I${includedir}
```



pkg-config命令的用途是：

你在Linux下写程序的时候，编译不需要头文件，链接需要动态库文件。

这些文件在哪里呢？

不太清楚。

这个时候，就需要pkg-config来发挥作用了。

查看头文件路径：

```
$ pkg-config --cflags gstreamer-1.0
-pthread -I/home/teddy/tools/install/gstreamer/include/gstreamer-1.0 -I/usr/local/include -I/usr/include/glib-2.0 -I/usr/lib/i386-linux-gnu/glib-2.0/include
```

查看依赖的库

```
$ pkg-config --libs gstreamer-1.0
-L/home/teddy/tools/install/gstreamer/lib -lgstreamer-1.0 -lgobject-2.0 -lglib-2.0
```

写Makefile这么写：

```
CFLAGS=`pkg-config --cflags --libs gstreamer-1.0`
all:
	gcc test.c $(CFLAGS)
```





参考资料

1、PKG_CONFIG_PATH和PKG_CONFIG的路径设置问题

https://blog.csdn.net/kartorz/article/details/3532570

