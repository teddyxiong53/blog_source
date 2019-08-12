---
title: gio（1）
date: 2019-08-03 17:17:19
tags:
	- gio

---

1

进行各种io操作。例如对socket的封装。

#写gio应用

关于线程，GDBus有自己的私有的工作线程，所以使用了GDBus的应用，都至少有3个线程。

关于异步编程，gio应用函数大多有2个版本：同步版本和异步版本。异步版本的函数，都用async做后缀的。

避免在主循环里使用同步函数。这样会影响消息的分发。

有些函数，例如gdbus-codegen生成的函数，默认是异步版本，而是把同步版本的后面加上sync后缀。

相关的类有GAsyncResult和GTask。

# 编译gio应用

头文件和库，通过pkg-config gio-2.0来获取。如果想要使用GUnixInputStream这些，则需要gio-unix-2.0。

# 运行gio应用

除了glib需要的环境变量。gio还另外需要一些环境变量。



api分类

```
文件操作
文件监控
文件相关工具
异步io
数据转换
io stream
文件类型和应用
磁盘卷和驱动
图标
可能失败的初始化
子进程
底层网络支持
上层网络应用
ssl支持
dns解析
底层dbus支持
上层dbus支持
设置
资源
权限
数据模型
应用支持
扩展io
工具

```



参考资料

1、GIO (Gnome Input/Output)

https://developer.gnome.org/gio/stable/

2、Glib实现Socket通信

https://blog.csdn.net/Hu_yilang/article/details/83419015