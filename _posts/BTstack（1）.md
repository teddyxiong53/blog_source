---
title: BTstack（1）
date: 2018-12-11 19:17:12
tags:
	- 蓝牙

---



--

# 基本信息

需要的目标板提供这些东西就可以工作：

1、串口。

2、CPU。

3、clock实现。



有几个缩写要先明确一下：

1、H2，是HCI USB 。

2、H4 。是HCI UART

3、H5。三线UART 。

我现在只管usb的。



手册章节

```
1、welcome信息。
2、quick start
	通用工具
	从github下载btstack代码
	开始
3、btstack架构
	单线程设计
	不阻塞
	不人为限制buffer
	静态内存
4、怎样配置btstack
	在btstack_config.h里配置
	HAVE_XX宏
	ENABLE_XX宏
	HCI控制器
	内存配置指令
	nvm指令
	源代码结构
	运行loop配置
	HCI传输配置
	服务
	packet handle配置
	蓝牙HCI包日志
5、协议
	HCI
	L2CAP
	RFCOMM
	SDP
	BNEP
	ATT
	SMP
6、profile
	GAP
	SPP
	PAN
	HSP
	HFP
	GAP LE
	GATT
7、实现GATT服务
8、嵌入式example
	一大堆的例子
9、HCI接口
10、移植到其他平台
```





在我的Ubuntu笔记本上运行。

需要先安装libusb。

```
sudo apt-get install gcc git libusb-1.0 pkg-config
```

然后在btstack/port/libusb目录下，make。

这个会自动把所有的example都编译的，并且把二进制生成到当前目录下。

运行其中一个例子：

```
teddy@teddy-ThinkPad-SL410:~/work/bt/btstack/port/libusb$ sudo ./le_counter 
Packet Log: /tmp/hci_dump.pklg
BTstack counter 0001
USB Path: 01
BTstack up and running on 00:1A:7D:DA:71:13.
```

可以看到可以正常运行。

我的蓝牙适配器是CSR的。

我们看看这个le_counter的代码是怎么写的。

main函数是在libus/main.c里。这里面调用了btstack_main这个函数在每个example里。



看看libusb目录下的btstack_config.h的内容：

```
HAVE_XX宏有4个：
1、有malloc。
2、有posix file no
3、有btstack stdin
4、有posix time
ENABLE_XX宏有：
1、使能ble。
2、使能经典蓝牙。
3、使能hfp 
4、
```

HAVE_PORTAUDIO这个有效。

当前btstack_memory_init这个函数相当于空的。里面的多个宏都没有生效。

可以通过gdb调试看到。



运行a2dp_sink_demo的例子。在手机上可以搜索到一个A2DP Sink Demo的蓝牙名字，可以连接上来。

然后播放歌曲。打印如下。当然实际上没有声音播放出来。这个不管。

```
teddy@teddy-ThinkPad-SL410:~/work/bt/btstack/port/libusb$ sudo ./a2dp_sink_demo 
Packet Log: /tmp/hci_dump.pklg
Starting BTstack ...
USB Path: 01
BTstack up and running on 00:1A:7D:DA:71:13.
A2DP Sink demo: received SBC codec configuration.
Received SBC configuration:
    - num_channels: 2
    - sampling_frequency: 48000
    - channel_mode: 1
    - block_length: 16
    - subbands: 8
    - allocation_method: 1
    - bitpool_value [2, 51] 

A2DP_SUBEVENT_STREAM_ESTABLISHED 86, 0 
A2DP Sink demo: streaming connection is established, address B4:0B:44:F4:16:8D, a2dp cid 0x56, local_seid 1
A2DP Sink demo: stream started, a2dp cid 0x56, local_seid 1
A2DP Sink demo: stream paused, a2dp cid 0x56, local_seid 1
WAV Writer: Decoding done. Processed totaly 5410 frames:
 - 5410 good
 - 0 bad
WAV Writer: Written 5410 frames to wav file: avdtp_sink.wav
```

这个例子的内容比较多。

最后hci的发送，调用的是usb_send_packet。这个跟每个平台有关系了。

最后调用libusb_submit_transfer。

# a2dp_sink_register_packet_handler 和a2dp_sink_register_media_handler 这2个处理函数的用途

`a2dp_sink_register_packet_handler` 和 `a2dp_sink_register_media_handler` 是 **BTstack** 蓝牙协议栈中用于注册回调函数的函数。这两个函数主要用于 **A2DP Sink**（音频接收端）的功能实现。

1. **`a2dp_sink_register_packet_handler`：**
   
   - 用途：注册处理 A2DP Sink 相关事件的回调函数。
   - 工作原理：当 BTstack 接收到与 A2DP Sink 相关的事件时，会调用注册的回调函数来处理这些事件。
   - 例如，当 A2DP Sink 收到音频数据包时，注册的 `a2dp_sink_register_packet_handler` 回调函数会被 BTstack 调用，从而可以在回调函数中处理接收到的音频数据包。

2. **`a2dp_sink_register_media_handler`：**
   
   - 用途：注册处理 A2DP Sink 媒体数据的回调函数。
   - 工作原理：用于处理音频流的数据，例如解码、播放等。
   - 当 A2DP Sink 收到音频流时，注册的 `a2dp_sink_register_media_handler` 回调函数会被调用，以便对接收到的音频数据进行进一步的处理，如解码和播放。

这两个函数的作用是将应用程序中定义的回调函数注册到 BTstack 中，以便在特定事件发生时得到通知并处理相应的数据。通过这种机制，开发者可以自定义处理 A2DP Sink 相关事件和音频数据的行为，实现音频接收端的功能。

# hci_stack_t

这个可以算是蓝牙协议栈hci内涵的直观体现了。

```
btstack_packet_handler_t 类型的处理函数
	acl_packet_handler
	sco_packet_handler
	iso_packet_handler
	event_handlers
一些链表：
	iso_streams
	le_audio_bigs
```



# l2cap_acl_handler

```c
    if (conn->address_type == BD_ADDR_TYPE_ACL){
        l2cap_acl_classic_handler(handle, packet, size);
    } else {
        l2cap_acl_le_handler(handle, packet, size);
    }
```

从这里也可以看出，acl有经典蓝牙和ble这2种。



# 参考资料

1、libusb安装

https://github.com/bluekitchen/btstack/tree/master/port/libusb

2、第06节-开源蓝牙协议BTStack框架分析

这个作者总结了韦东山的蓝牙视频笔记。挺好的。

https://www.cnblogs.com/-glb/p/11617659.html

3、

https://blog.csdn.net/happygrilclh/article/details/100743580