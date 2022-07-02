---
title: Linux之wpa_supplicant架构分析
date: 2022-04-08 10:44:11
tags:
	- Linux

---

--

```
wpa supplicant 在启动时，启动命令可以带有很多参数，目前我们的启动命令如下：
wpa_supplicant /system/bin/wpa_supplicant -Dwext -ieth0 -c/data/wifi/wpa_supplicant.conf -f/data/wifi/wpa_log.txt
```

wpa_supplicant对于启动命令带的参数，用了两个数据结构来保存，

一个是 wpa_params, 另一个是wpa_interface.

这主要是考虑到wpa_supplicant是可以同时支持多个网络接口的。

wpa_params数据结构

主要记录与网络接口无关的一些参数设置。

而每一个网络接口就用一个wpa_interface数据结构来记录。



\2. wpa_supplicant 初始化流程
2.1. main()函数：
在这个函数中，主要做了四件事。
a. 解析命令行传进的参数。
b. 调用wpa_supplicant_init()函数，做wpa_supplicant的初始化工作。
c. 调用wpa_supplicant_add_iface()函数，增加网络接口。
d. 调用wpa_supplicant_run()函数，让wpa_supplicant真正的run起来。



2.4. wpa_supplicant_run()函数：
初始化完成之后，让wpa_supplicant的main event loop run起来。
在wpa_supplicant中，有许多与外界通信的socket，它们都是需要注册到eloop event模块中的，具体地说，就是在eloop_sock_table中增加一项记录，其中包括了sock_fd, handle, eloop_data, user_data。
eloop event模块就是将这些socket组织起来，统一管理，然后在eloop_run中利用select机制来管理socket的通信。



\3. Wpa_supplicant提供的接口
从通信层次上划分，wpa_supplicant提供向上的控制接口 control interface，用于与其他模块（如UI）进行通信，其他模块可以通过control interface 来获取信息或下发命令。Wpa_supplicant通过socket通信机制实现下行接口，与内核进行通信，获取信息或下发命令。

上行接口
Wpa_supplicant提供两种方式的上行接口。一种基于传统dbus机制实现与其他进程间的IPC通信；另一种通过Unix domain socket机制实现进程间的IPC通信。



Dbus接口
该接口主要在文件“ctrl_iface_dbus.h”，“ctrl_iface_dbus.c”，“ctrl_iface_dbus_handler.h”和“ctrl_iface_dbus_handler.c”中实现，提供一些基本的控制方法。



 Unix domain socket 接口
该接口主要在文件“wpa_ctrl.h”，“wpa_ctrl.c”，“ctrl_iface_unix.c”，“ctrl_iface.h”和“ctrl_iface.c”实现。



“l2_packet.h”和“l2_packet_linux.c”主要用于实现PF_PACKET socket接口，通过该接口，wpa_supplicant可以直接将802.1X packet发送到L2层，而不经过TCP/IP协议栈。



参考资料

1、

https://blog.csdn.net/hubinbin595959/article/details/105091310