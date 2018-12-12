---
title: 蓝牙之Linux下实现局域网
date: 2018-12-12 11:20:35
tags:
	- 蓝牙

---



蓝牙的局域网，也叫PAN，Personal Area Network。个域网。

在btstack的例子里有个panu_demo.c。也是做这个的。

在bluetooth_sdp.h里，service类型宏定义这里可以看到：

```
#define BLUETOOTH_SERVICE_CLASS_HEADSET_AUDIO_GATEWAY_AG                           0x1112 // Headset Profile (HSP)
#define BLUETOOTH_SERVICE_CLASS_WAP                                                0x1113 // Interoperability Requirements for Bluetooth technology as a WAP, Bluetooth SIG [DEPRECATED]
#define BLUETOOTH_SERVICE_CLASS_WAP_CLIENT                                         0x1114 // Interoperability Requirements for Bluetooth technology as a WAP, Bluetooth SIG [DEPRECATED]
#define BLUETOOTH_SERVICE_CLASS_PANU                                               0x1115 // Personal Area Networking Profile (PAN) NOTE: Used as both Service Class Identifier and Profile Identifier for PANU role.
#define BLUETOOTH_SERVICE_CLASS_NAP                                                0x1116 // Personal Area Networking Profile (PAN) NOTE: Used as both Service Class Identifier and Profile Identifier for NAP role.

```



# 参考资料

1、实用技巧：组建Linux下的个人蓝牙局域网

http://www.voidcn.com/article/p-vicbdcws-zr.html

2、Linux平台下架建个人蓝牙局域网

https://www.linuxidc.com/Linux/2008-02/11249.htm