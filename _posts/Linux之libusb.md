---
title: Linux之libusb
date: 2018-12-12 12:00:35
tags:
	- Linux

---



看btstack的源代码，我看的port版本是libusb版本的，最后是调用到libusb的函数进行的数据收发。

那么最后libusb里干了些什么呢？

源代码在这里：https://github.com/libusb/libusb

这里面有些简单的example可以看看。

lsusb这个命令就是基于libusb来做的。

Ubuntu下安装：

```
sudo apt-get install libusb-1.0-0-dev
```

链接的时候，加上-lusb-1.0就好。

需要包含的头文件是：

```
#include <libusb-1.0/libusb.h>
```

官网：https://libusb.info/

libusb是一个跨平台的用户态的库，用来访问usb设备。

当前版本是1.0。之前的版本0.1 ，这个版本已经过时了。

需要Linux支持usbfs。

代码在这里：

Https://github.com/libusb/libusb

使用了libusb的项目有：

usbutils：Linux的usb工具包。

btstack：轻量级蓝牙协议栈。

libuvc

提供这些语言的binding

pyusb



usb驱动分为通过usbfs操作设备的用户空间驱动，内核空间的内核驱动。两者不能同时进行，否则容易引发对共享资源访问的问题，死锁！使用了内核驱动，就不能在usbfs里驱动该设备。

libusb中须要先detach内核驱动后，才能claim interface，否则claim会返回的vice busy的错误。

如果你不dettach，也不claim interface，也能使用libusb对设备进行访问，但是，容易导致内核usbfs瘫痪，这是不允许的。




参考资料

1、官方wiki

https://github.com/libusb/libusb/wiki

2、使用usbfs与内核驱动之间的冲突

https://blog.csdn.net/crazyleen/article/details/7062327