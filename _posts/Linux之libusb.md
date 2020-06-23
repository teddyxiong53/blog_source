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



这种新的协议的问题一般是采用后者来实现，因为内核主线是不会采纳不通用的驱动代码的。所以为了不一直为所有的版本内核都添加自己的驱动，可以在用户空间直接USB通信。这才是大家都好的结局。

 这个时候大家猛然发现已经在内核中实现的基于printer协议的打印驱动程序也可以采用这个方法直接在用户空间USB通信实现，这样就可以完全和系统无关了，内核只要有usb通信协议就好了。上半场已经捋顺了，下面说说下半场。

方向明确了，如何实现，这时候大家发现了libusb，libusb可以实现用户空间直接和usb设备直接通信。这样大家都采用了基于libusb的免驱模式，如实说就是免掉内核中的驱动模式。



Linux 平台上的usb驱动开发，主要有内核驱动的开发和基于libusb的无驱设计。

*libusb是基于用户空间的usb库。libusb* 设计了一系列的外部*API* 为应用程序所调用，通过这些*API*应用程序可以操作硬件，从*libusb*的源代码可以看出，这些*API* 调用了内核的底层接口，和*kernel driver*中所用到的函数所实现的功能差不多，**只是*libusb*更加接近*USB* 规范。使得*libusb*的使用也比开发内核驱动相对容易的多。**





usb驱动分为通过usbfs操作设备的用户空间驱动，内核空间的内核驱动。两者不能同时进行，否则容易引发对共享资源访问的问题，死锁！使用了内核驱动，就不能在usbfs里驱动该设备。

libusb中须要先detach内核驱动后，才能claim interface，否则claim会返回的vice busy的错误。

如果你不dettach，也不claim interface，也能使用libusb对设备进行访问，但是，容易导致内核usbfs瘫痪，这是不允许的。




参考资料

1、官方wiki

https://github.com/libusb/libusb/wiki

2、使用usbfs与内核驱动之间的冲突

https://blog.csdn.net/crazyleen/article/details/7062327

3、Libusb简介及例子

https://blog.csdn.net/hfyutdg/article/details/83896116

4、libusb的嵌入式移植

https://blog.csdn.net/tianruxishui/article/details/37903579

5、libusb函数说明

很好。

https://blog.csdn.net/wince_lover/article/details/70337809