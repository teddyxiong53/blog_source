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

dbus就是对socket的封装。



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

主要用来进程间**函数调用**和进程间**信号广播**。



dbus的特点：

1、低延迟。

2、低开销。

3、高可用。

协议是二进制的，避免了序列化的过程。通信效率高。

因为主要是用于本机内部通信，所以采用二进制带来的好处大于坏处。

支持异步操作。

dbus易于使用，因为它是基于消息，而不是字节流。



总线有两种，一个是system bus，一个是session bus。

本质上，dbus是一个对等的协议。

每个消息都一个源地址和目的地址。



看dbus代码里的readme的说明。

版本系统，跟Linux内核一个风格，偶数的表示稳定版本，奇数版本表示开发版本。



dbus默认提供了一些工具。

dbus-monitor和dbus-send。可以用来测试。



系统里的dbus工具有：

````
dbus-binding-tool
dbus-daemon
	--session等价于：--config-file=/usr/share/dbus-1/session.conf
	
dbus-monitor
	这个只有5个选项。比较简单。
	--system：监控系统bus的消息。
	--session：监控用户session bus的消息。默认是这个。
	--profile：不指定，就是classic模式。这个是精简模式。
	--monitor：监控输出模式。默认就是这个。
dbus-send
dbus-uuidgen
dbus-cleanup-sockets
dbus-launch
dbus-run-session
dbus-update-activation-environment
````



```
dbus-send --print-reply --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ListNames
```



dbus-glib和GDBus的区别



dbus是很多重要系统的底层，需要加深理解。

例如bluez就大量使用了dbus。



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

8、dbus-glib示例说明

https://wenku.baidu.com/view/9a352d1152d380eb62946d67.html?sxts=1564551835283

9、dbus基础知识

https://wenku.baidu.com/view/0804b93283c4bb4cf7ecd1a9.html?from=search

10、DBus API的使用

https://my.oschina.net/u/994235/blog/113238

11、DBUS及常用接口介绍

https://blog.csdn.net/mr_wangning/article/details/60324291

12、D-Bus Documentation

https://dbus.freedesktop.org/doc/api/html/index.html

13、DBUS基础知识

https://www.cnblogs.com/wzh206/archive/2010/05/13/1734901.html

14、dbus-glib 和 GDBus 的区别

https://www.cnblogs.com/LubinLew/p/dbus-glib_and_GDBus.html