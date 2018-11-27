---
title: 蓝牙之rfcomm
date: 2018-11-27 14:59:35
tags:
	- 蓝牙

---



看蓝牙相关资料，看到rfcomm这个东西。了解一下。

rfcomm是蓝牙协议栈里的一个协议。

这个协议很简单，是在无线上模拟了RS232协议。

rfcomm可以支持2个蓝牙模块之间同时进行60路通信。

```
/* ---- RFCOMM sockets ---- */
struct sockaddr_rc {
	sa_family_t	rc_family;
	bdaddr_t	rc_bdaddr;
	u8		rc_channel;
};
```

```
#define BTPROTO_L2CAP	0
#define BTPROTO_HCI	1
#define BTPROTO_SCO	2
#define BTPROTO_RFCOMM	3
#define BTPROTO_BNEP	4
#define BTPROTO_CMTP	5
#define BTPROTO_HIDP	6
#define BTPROTO_AVDTP	7
```



参考资料

1、RFCOMM

https://www.cnblogs.com/fbli/p/5930383.html

2、蓝牙RFCOMM剖析（一）

https://blog.csdn.net/xiaoxiaopengbo/article/details/51446171