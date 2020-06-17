---
title: 蓝牙之Linux开发
date: 2018-07-23 22:28:29
tags:
	- 蓝牙

---



**bluez的代码基础部分都是由高通的Maxim来完成的。**

包括HCI、L2CAP、RFCOMM和基本socket的实现。

还有一部分的代码是由Nokia提供的。

bluez是如何实现协议栈的呢？

分为2个部分：

1、kernel层。

除了底部的硬件层，软件上是从HCI层开始的。

bluez是依托于socket的。

首先创建了一个协议类型PF_BLUETOOTH。

2、应用层。

**虽然kernel里已经实现了socket。但是应用层如果用ioctl来进行控制，很不方便，所以bluez就进行了一些封装，提供了一些简单好用的应用层api。**



# 内核里的蓝牙相关代码

## 头文件

头文件在include/net/bluetooth目录下。

```
├── bluetooth.h socket相关。
├── hci_core.h 定义了hci_dev、hci_conn这些核心结构体，很复杂。
├── hci.h   这个就是定义了很多的的宏和小的结构体。都是进行协议分析的。
├── hci_mon.h
├── hci_sock.h  hci_dev_info hci_conn_info
├── l2cap.h
├── mgmt.h
├── rfcomm.h
└── sco.h
```

应用层编程，经常包含：

```
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>
```



### bluetooth.h

协议种类：

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

socket分层：

```
#define SOL_HCI		0
#define SOL_L2CAP	6
#define SOL_SCO		17
#define SOL_RFCOMM	18
```

打印函数：

```
#define BT_INFO(fmt, ...)	bt_info(fmt "\n", ##__VA_ARGS__)
#define BT_WARN(fmt, ...)	bt_warn(fmt "\n", ##__VA_ARGS__)
#define BT_ERR(fmt, ...)	bt_err(fmt "\n", ##__VA_ARGS__)
#define BT_DBG(fmt, ...)	pr_debug(fmt "\n", ##__VA_ARGS__)
```

连接状态

```
enum {
	BT_CONNECTED = 1, /* Equal to TCP_ESTABLISHED to make net code happy */
	BT_OPEN,
	BT_BOUND,
	BT_LISTEN,
	BT_CONNECT,
	BT_CONNECT2,
	BT_CONFIG,
	BT_DISCONN,
	BT_CLOSED
};
```

地址类型

```
typedef struct {
	__u8 b[6];
} __packed bdaddr_t;
```

特殊地址：

```
#define BDADDR_ANY  (&(bdaddr_t) {{0, 0, 0, 0, 0, 0}})
#define BDADDR_NONE (&(bdaddr_t) {{0xff, 0xff, 0xff, 0xff, 0xff, 0xff}})
```

地址操作函数：

```
bacmp
bacpy
baswap

```

蓝牙sock

```
struct bt_sock {
	struct sock sk;
	struct list_head accept_q;
	struct sock *parent;
	unsigned long flags;
	void (*skb_msg_name)(struct sk_buff *, void *, int *);
};
```

## 代码文件

主要在net/bluetooth目录下。







# 参考资料

1、实战Linux Bluetooth编程

https://blog.csdn.net/hanmengaidudu/article/details/17028375

2、linux下蓝牙开发(bluez应用)

https://www.cnblogs.com/liangjf/p/8677563.html

3、用树莓派玩转蓝牙

https://www.cnblogs.com/vamei/p/6753531.html

4、

https://zzk.cnblogs.com/s?t=b&w=%E8%93%9D%E7%89%99Linux%E5%BC%80%E5%8F%91

5、实战Linux Bluetooth编程（一） 协议栈概述

这个是系列文章，本链接是最原始的。网上很多是转载这里的。2009年写的。

http://blog.sina.com.cn/s/blog_602f87700100e0vb.html

6、Linux bluetooth setup with bluez and hcitool

https://www.pcsuggest.com/linux-bluetooth-setup-hcitool-bluez/