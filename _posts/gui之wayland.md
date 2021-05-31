---
title: gui之wayland
date: 2021-05-28 15:09:11
tags:
	- gui

---

--

简单地说，Wayland是一套display server(Wayland compositor)与client间的通信协议，而Weston是Wayland compositor的参考实现。

其官网为http://wayland.freedesktop.org/。

它们定位于在Linux上替换X图形系统。

X图形系统经历了30年左右的发展，其设计在今天看来已略显陈旧。

在X系统中，X Server作为中心服务，连接clien和硬件以及compositor。

**但时至今日，原本在X Server中做的事很多已被移到kernel或者单独的库中，**

因此X Server就显得比较累赘了。

**Wayland在架构上去掉了这个中间层，**

将compositor作为display server，**使client与compositor直接通信**，从而在灵活性和性能等方面上能够比前辈更加出色。



Wayland既可以用于传统的桌面又适用于移动设备，

已经被用于Tizen，Sailfish OS等商业操作系统，

同时越来越多的窗口和图形系统开始兼容Wayland协议。

Wayland**基于domain socket**实现了一套display server与client间通信的库

（简单的基于例子的介绍可以参见http://blog.csdn.net/jinzhuojun/article/details/40264449），

**并且以XML形式定义了一套可扩展通信协议。**

这个协议分为Wayland核心协议和扩展协议（位于Weston中）。

**Weston作为Wayland compositor的参考实现，一般和Wayland同步发布。**

其它Wayland compositor实现还有如mutter, Kwin, Lipstick, Enlightenment, Clayland等。





参考资料

1、

https://blog.csdn.net/melody157398/article/details/91349848