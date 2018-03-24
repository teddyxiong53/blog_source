---
title: qemu（一）
date: 2018-03-23 18:50:35
tags:
	- qemu

---



一直觉得虚拟机很神奇。qemu可以是一个很好的切入点，我也有很多的使用上的问题，希望可以在代码里得到解答。

当前我都是在命令行下面使用qemu的。其实可以试一下图形化界面的情况。

我就试一下在windows的使用。看看有什么不一样的地方。

下载地址在这里。

http://qemu.weilnetz.de/w64/2018/

安装程序98M。不大。下载是2.12版本的。

安装后，还是只能命令行运行。然后是有问题。

```
D:\Program Files\qemu>qemu-system-i386
Unexpected error in aio_context_set_poll_params() at /home/stefan/src/qemu/repo.or.cz/qemu/ar7/util/aio-win32.c:413:
qemu-system-i386: AioContext polling is not implemented on Windows
```

解决的办法有，就是降低qemu的版本。

我发现我之前运行



下载qemu代码。解压后，大概260M。文件24000个左右。是挺多的，跟linux源代码的规模差不多了。

可以在各种平台上编译，我就在linux上编译。



```
ERROR: glib-2.22 gthread-2.0 is required to compile QEMU
```





