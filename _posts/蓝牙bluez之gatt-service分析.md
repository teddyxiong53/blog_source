---
title: 蓝牙bluez之gatt-service分析
date: 2020-03-27 16:24:11
tags:
	- 蓝牙

---

1

bluez代码下有一个gdbus目录。

下面有5个C文件和一个头文件。

头文件是gdbus.h。里面定义了：

```
1、引用了2个头文件。
	#include <dbus/dbus.h>
	#include <glib.h>
	感觉这个模块也就是把dbus和glib进行包装使用。
2、定义了5个结构体。
	GDBusArgInfo
	GDBusMethodTable
	GDBusSignalTable
	GDBusPropertyTable
	GDBusSecurityTable
		就是4个表。方法表、信号表、属性表、安全表。
	结构体定义，都是GDBus开头。
	函数定义，都是 g_dbus开头。
	
```

5个C文件

```
client.c
	g_dbus_client_new 创建一个GDBusClient
	
mainloop.c
	//创建一个dbus的connection的方法。
	connection = g_dbus_setup_bus(DBUS_BUS_SYSTEM, NULL, NULL);
```



基于dbus技术的编程框架有4种：

1、glib-dbus。

2、gdbus。

3、qtdbus。最简单。

4、dbus-python。

gdbus和glib-dbus都是gnu开发的。

gdbus可以认为是glib-dbus的升级版本。

所以我们就看看gdbus的用法。





参考资料

1、基于GDBus技术的IPC通信编程详解(1)

https://blog.csdn.net/adlindary/article/details/80167840