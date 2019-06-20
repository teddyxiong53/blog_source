---
title: Linux之dbus
date: 2018-09-10 17:36:31
tags:
	- Linux

---



dbus能不能移植到嵌入式系统里？如何移植？

如何写一个简单程序来测试dbus工作是否正常？

怎样写一个基本程序来理解dbus的原理？

为什么需要dbus？



dbus是一个为App之间通信的消息总线系统。用于进程间通信。跟共享内存、信号量这些的一个类型的东西。

采用了3层架构。

1、一个库文件libdbus。我们写app，链接这个库，就可以。

2、一个守护进程。所有消息，都通过这个守护进程来转发。

3、跟特定库或者语言的绑定，例如跟Python的绑定，跟glib的绑定，跟qt的绑定。

官方也不建议直接使用dbus，而是使用包装过的。这样用起来会简单些。

```
dbus-daemon --system
```



看树莓派的情况。

```
root@raspberrypi:/etc/dbus-1# tree
.
├── session.d
└── system.d
    ├── avahi-dbus.conf
    ├── bluetooth.conf
    ├── Mountall.Server.conf
    ├── org.freedesktop.hostname1.conf
    ├── org.freedesktop.locale1.conf
    ├── org.freedesktop.login1.conf
    ├── org.freedesktop.network1.conf
    ├── org.freedesktop.PolicyKit1.conf
    ├── org.freedesktop.RealtimeKit1.conf
    ├── org.freedesktop.resolve1.conf
    ├── org.freedesktop.systemd1.conf
    ├── org.freedesktop.timedate1.conf
    ├── pulseaudio-system.conf
    └── wpa_supplicant.conf

2 directories, 14 files
```





buildroot里，可以选配dbus的支持。

在hardware handling下面。



这些conf文件，都是xml格式的。

现在我关注的蓝牙这个部分。

看看蓝牙dbus如何使用的。



多对多的dbus消息都通过dbus后台进程进行中转。相当于一个消息路由。

是一种进程间通信机制，支持一对一和一对多的对等通信。

dbus的主要概念是总线。

连接到总线的消息可以通过总线发送或者接收消息。

消息可以分为4种。

```
1、method call消息。
	触发一个函数调用。
2、method return消息。
	触发函数调用返回的结果。
3、error消息。
	触发的函数调用返回一个异常。
4、signal消息。
	通知，就是触发事件。这个跟上面三个不同。
```

主要用来进程间**函数调用**和进程键**信号广播**。



dbus的特点：

1、低延迟。

2、低开销。

3、高可用。

协议是二进制的，避免了序列化的过程。通信效率高。



总线有两种，一个是system bus，一个是session bus。

本质上，dbus是一个对等的协议。

每个消息都一个源地址和目的地址。



看dbus代码里的readme的说明。

版本系统，跟Linux内核一个风格，偶数的表示稳定版本，奇数版本表示开发版本。



dbus默认提供了一些工具。

dbus-monitor和dbus-send。可以用来测试。



# 参考资料

1、DBus 入门与应用 －－ DBus 的 C 编程接口

https://www.cnblogs.com/liyiwen/archive/2012/12/02/2798876.html

2、官方文档

https://dbus.freedesktop.org/doc/api/html/annotated.html

3、和菜鸟一起学linux之DBUS基础学习记录

https://blog.csdn.net/eastmoon502136/article/details/10044993

4、dbus通信与接口介绍

https://www.cnblogs.com/klb561/p/9135642.html

5、

https://www.cnblogs.com/chenxf0619/p/4829253.html

6、

https://dbus.freedesktop.org/doc/dbus-tutorial.html

7、dbus-send以及dbus-monitor工具的使用方法示例

https://www.xuebuyuan.com/3188840.html

