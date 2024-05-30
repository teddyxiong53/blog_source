---
title: 蓝牙之Linux开发
date: 2018-07-23 22:28:29
tags:
	- 蓝牙

---

--

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

在 Linux 内核源代码中，与蓝牙协议相关的文件分布在几个目录中。

主要涉及蓝牙协议栈的实现、驱动程序和用户空间接口。

以下是主要的目录及其内容简介：

1. **`net/bluetooth/`**：
   - 这个目录包含了蓝牙协议栈的核心实现。
   - 主要文件：
     - `af_bluetooth.c`：蓝牙协议族的实现。
     - `hci_core.c`：HCI（Host Controller Interface）核心处理。
     - `hci_event.c`：HCI 事件处理。
     - `hci_sock.c`：HCI 套接字处理。
     - `l2cap_core.c`：L2CAP（Logical Link Control and Adaptation Protocol）核心处理。
     - `l2cap_sock.c`：L2CAP 套接字处理。
     - `sco.c`：SCO（Synchronous Connection-Oriented）链路处理。
     - `mgmt.c`：蓝牙管理接口实现。

2. **`drivers/bluetooth/`**：
   - 这个目录包含了各种蓝牙设备的驱动程序。
   - 主要文件：
     - `btusb.c`：USB 蓝牙设备的驱动程序。
     - `hci_ldisc.c`：HCI 线路规程驱动。
     - `hci_uart.c`：HCI UART 驱动。
     - 其他特定芯片的驱动程序文件（如 `hci_bcm.c`、`hci_intel.c`、`hci_qca.c` 等）。

3. **`include/net/bluetooth/`**：
   - 这个目录包含了蓝牙协议栈的头文件。
   - 主要文件：
     - `bluetooth.h`：蓝牙协议的通用定义。
     - `hci_core.h`：HCI 核心定义。
     - `l2cap.h`：L2CAP 协议定义。
     - `sco.h`：SCO 协议定义。
     - `mgmt.h`：蓝牙管理接口定义。

4. **`include/uapi/linux/`**：
   - 这个目录包含了用户空间 API 的头文件，蓝牙相关的头文件主要有：
     - `bluetooth.h`：蓝牙协议的通用用户空间 API 定义。
     - `hci.h`：HCI 用户空间 API 定义。
     - `l2cap.h`：L2CAP 用户空间 API 定义。
     - `sco.h`：SCO 用户空间 API 定义。

5. **`net/bluetooth/hci_**` 相关文件：
   - 这些文件具体处理 HCI 的各个方面，如 `hci_event.c` 处理 HCI 事件，`hci_conn.c` 处理 HCI 连接等。

这些文件和目录共同实现了 Linux 内核中蓝牙协议的支持，包括底层驱动、协议栈、用户空间接口等各个方面。通过这些文件，Linux 能够支持多种蓝牙设备和协议，实现设备发现、连接、数据传输等功能。



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