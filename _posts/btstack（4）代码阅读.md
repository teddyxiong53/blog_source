---
title: btstack（4）代码阅读
date: 2018-12-20 15:18:35
tags:
	- 蓝牙
---



我觉得奇怪，为什么avdtp的直接调用了l2cap_send函数呢？

这样怎么体现分层呢？

各个层都看到有对L2CAP的函数的调用。

# a2dp_sink_demo

初始化代码：

```
1、l2cap_init。底层初始化。
2、a2dp_sink_init。
3、a2dp_sink注册packet handler。
4、a2dp_sink注册media handler。
5、a2dp_sink创建stream endpoint。
6、avrcp_controller初始化。
7、avrcp_controller注册packet handler。
8、sdp_init。
9、a2dp_sink创建sdp record。
10、sdp注册服务。
11、avrcp_controller创建sdp record。
12、sdp注册avrcp controller服务。
13、gap_set_local_name为A2DP Sink Demo
14、gap_discoverable_control(1)
15、gap_set_class_of_device(0x200408);
16、hci_add_event_handler。
```



l2cap_init函数

```
l2cap_channels单链表，把l2cap_fixed_channel_connectionless加进去。
然后添加了l2cap_fixed_channel_att和l2cap_fixed_channel_sm。

```



btstack_run_loop_t

```
hci_stack->bondable = 1; 
```



platform 

port

chipset

跟具体的板子相关的目录有这3个，分别放了什么内容？

chipset：主要负责底层引脚配置这些。

```
填充btstack_chipset_t结构体。
	主要函数：
		init，没干啥。
		next_command：紧跟init执行一些操作。
		设置蓝牙地址
		设置波特率。
```

port：main函数在这里。

```

```

platform：主要是一个run_loop结构体。是主循环，基于select。分析入口在这里。

```

```



add_data_source，这个添加数据源，会遍历单链表。

目前对于sink_demo，有2个数据源。

```
一个是uart串口。
btstack_run_loop_add_data_source(&transport_data_source);
一个是stdin。
```

2个数据，自己注册处理函数给loop。就是里面的process指针。



把日志分析一下。

从host到controller的，叫cmd。

从controller到host的，叫evt。

```
1、cmd： 00 03 0c 00 
HCI复位命令。最前面的00表示是cmd。0x0c03表示reset。00表示长度为0 。
2、evt：01 0e 04 01 03 0c 00
HCI复位命令的回复。
01表示evt。0e表示命令完成。04表示长度4字节。01表示命令包个数为1。0c03表示reset。00表示成功。
3、cmd：00 18 fc 06 00 00 00 10 0e 00
设置波特率命令。
00表示是cmd。fc18 是厂家命令，表示更新波特率。06表示长度。00 00 没用。000e1000表示921600的波特率。
4、不看了，就成功的。格式跟2的一样。
5、下载mini driver。博通特有的。
6、回复下载成功。
7、开始写firmware。
分了多次写，每次写得不多。

```

