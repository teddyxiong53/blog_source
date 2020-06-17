---
title: rtsp（1）
date: 2018-04-29 21:27:46
tags:
	- rtsp
typora-root-url: ..\
---



下面引用的代码主要是来自这里：https://github.com/teddyxiong53/Linux-C-Examples/tree/master/rtsp



rtsp在github上的相关开源代码有：

1、librtsp。有26个star。

https://github.com/ykst/librtsp

2、rtspserver

https://github.com/ashwing920/rtspserver

3、v4l2rtspserver



但一般做直播用RTSP RTMP，做点播用HTTP

RTMP和RTSP协议是流媒体协议。

RTMP协议是Adobe的私有协议,未完全公开，RTSP协议和HTTP协议是共有协议，并有专门机构做维护。

Adobe 收购 Macromedia 购以后，公布了这个协议的一部分，以备公共使用。



#流媒体定义

流媒体有广义和狭义的两种定义。

广义上是指，使得音频和视频形成稳定、连续的传输流和回放流的一系列技术、方法、协议的总和。

狭义上是指，相当于传统的下载播放方式而言，支持多媒体数据的实时传输和实时播放。



#流媒体协议

1、实时传输协议。RTP。

可以单播，也可以多播。

一般是基于UDP的。

RTP协议包括：RTP数据协议和RTP控制协议。

**RTSP位于RTP和RTCP之上。目的是通过IP网络有效地传输多媒体数据。**

## RTSP/RTP/RTCP关系

一句话概括，就是RTSP用来start、stop传输，RTP用来传输媒体数据，RTCP对RTP进行控制、同步。

RTSP里的setup方法，就确定了RTP/RTCP的端口。

RTSP里的play、pause、teardown，就控制了RTP的状态。

RTCP包括Sender Report和Receiver Report。用来进行音视频的同步。

RTSP还可以在HTTP上跑。



通常来说，RTSP提供UDP方式发送RTP流。当然，发送流媒体时，UDP往往是更好的选择。但是，在互联网上使用UDP方式发送流是不可能的。

使用udp方式，需要注意的一些问题：

1、基于udp，需要多打开一些端口。

2、当Internet上的路由器没有打开这些udp端口的时候，udp方式就走不通。

3、中间路由器很容易过滤或者忽略掉udp数据包。

4、udp本身不可靠。

如果使用tcp方式，则可以解决上面的问题。

1、控制和命令，都只需要经过554端口完成。

2、tcp包可靠。

3、tcp穿透中间路由器的能力更强。

但是tcp也有缺点：

**1、因为数据和控制交织在一起，RTP的封包和解包就更加复杂了。**

2、TCP会导致延迟。





#RTP协议

先看头部的构成。

对应的文档是RFC3550 。RFC1889是老版本。

在RFC3550里，不仅定义了RTP，还定义了配套的RTCP协议。

RTP不保证服务质量，由RTCP来保证。



RTP协议原理比较简单。负责对流媒体数据进行封包并实现媒体流的实时传输。



包头的结构是：

```
struct rtp_header {
    //byte0
    u8 csrc_len:4;
    u8 extension:1;//这个为1的话，表示扩展包头。
    u8 padding:1;//如果为1，表示表示包的尾部填充一个或者多个字节。
    u8 version:2;//目前的版本是2 。

    //byte1
    u8 payload:7;//负载类型。96表示H264这样。
    u8 marker:1;//对于视频，表示一帧的结束，对于音频，表示会话的开始。

    u16 seq_no;
    u32 timestamp;
    u32 ssrc;//sync src id。同步信源。
};
```



怎样重组乱序的数据包？

通过RTP包的seq no来排序。

怎样获得数据包的时序？

靠RTP包的时间戳。

声音和视频如何同步？

也是靠RTP包的时间戳。以及RTCP包里的绝对时间。

## NALU

NALU是网络抽象层单元的缩写。

是负载的第一个字节来确定类型。

```
bit0: F。H264里，这个bit必须为0 。
bit1-2: NRI。表示这个单元的重要性。00表示可以丢弃，没有什么影响。
bit3-7: 取值范围是0到31 。
	0：没有定义。
	1-23：单个NALU
	24：STAP-A 单一时间的组合包。
	25：STAP-B 单一时间的组合包。
	26：MTAP16 多个时间的组合包。
	27：MTAP24 多个时间的组合包。
	28：FU-A 分片的单元。
	29： FU-B 分片的单元。
	30-31：没有定义。
```



如果NALU对应的Slice为一帧的起始，用4个字节表示，就是0x 00 00 00 01 。

否则是用3个字节表示，就是0x 00 00 01 。

为了防止内部数据也出席这种00 00 00 01的数据，H.264加入了一种防止竞争的机制。

当检测到2个连续的00的时候，就会在后面插入一个03 。

解码的时候，检测到00 00 03 ，会把03 丢掉的。

所以00 00 00 01和00 00 01是可以用来做起始检测的。



rtp数据是用udp发送出去的。



NALU的类型：

```
#define H264_NAL_TYPE_NON_IDR 1
#define H264_NAL_TYPE_SLICE_A 2
#define H264_NAL_TYPE_SLICE_B 3
#define H264_NAL_TYPE_SLICE_C 4
#define H264_NAL_TYPE_IDR 5
#define H264_NAL_TYPE_SEI 6
#define H264_NAL_TYPE_SPS 7
#define H264_NAL_TYPE_PPS 8
```

我们建立点播环境。

打开wireshark抓包，就在filter那里填入h264就好了。







rtspd里没有看到明显写PPS、SPS这些东西。

https://zhuanlan.zhihu.com/p/27896239

这篇文章讲了pps、sps。



## rtp荷载H264码流

rtp包的负载部分，第一个字节是有特殊含义的。

表示了负载的类型。

1、单个NALU 。

也就是只有一个NALU 。

2、聚合包。

3、分片单元。

## FU-A分包方式

当NALU长度超过MTU的时候，就要对NALU进行分包。Fragmentation Units。简写为FU 。

是在RTP和负载之间，加入2个字节。

```
memcpy(nalu_buffer,&rtp_header,sizeof(rtp_header));
memcpy(nalu_buffer + 14,p_nalu_data,proc_size);
nalu_buffer[12] = fu_indic;
nalu_buffer[13] = fu_header;
```

```
fu_indic    = (nalu_header&0xE0)|28;//因为28号是FU-A的类型。
fu_end = (proc_size == data_left);
fu_header = nalu_header&0x1F;
if(fu_start)
fu_header |= 0x80;
else if(fu_end)
fu_header |= 0x40;
```



# RTSP协议

对应的rfc文档是：https://www.ietf.org/rfc/rfc2326.txt

RTSP协议在设计的时候，尽可能地参考了http协议。

这样做的原因有：

1、尽可能兼容现有的web基础结构。

因为这种考虑，所以http/1.1的扩展机制大部分都可以直接引入到rtsp里。



rtsp和http的区别：
1、很多防火墙都会屏蔽rtsp，http则一般不屏蔽。

2、rtsp适用于大数据量、高可用的流。例如直播事件，大型文件。

而http则适合小数据。



客户端和服务端的交互过程如下图。

![](/images/rtsp（1）-rtsp交互过程.png)

RTSP over UDP
对于udp模式，客户端发送了play之后，就打开了udp端口，用来接收服务端发来的RTP数据包。
服务端也会打开udp端口，用来发送RTP数据包。
UDP方式简单，但是容易丢包。

![](/images/rtsp（1）-udp方式.png)

RTSP over TCP
对于tcp模式，通过setup来指定传输方式，服务器返回同样数据以确定双方通过tcp方式来传输数据。

![](/images/rtsp（1）-tcp方式.png)

由于跟rtsp消息使用了同一个tcp端口，为了区分rtp包和rtcp包，增加了4个字节额外的字段，并通过特殊的标识符号“$”进行区分。

```
标识符 $    一个字节
通道号      一个字节
RTP/RTCP包大小   2个字节。
```



实现的rtsp server，主要功能是采集摄像头和麦克风的数据，进行H.264编码和AAC编码。对外提供rtsp直播流服务。

用udp的方式实现，在大码率的情况下，丢包严重，导致花屏现象很严重。



# RTCP协议

rtcp和rtp协议一起定义在1996年提出的RFC1889里。

二者一起工作。

## rtcp功能

1、为app提供会话质量或者广播性能质量信息。

这个是主要功能。

2、确定rtp用户源。

3、控制rtcp传输间隔。

4、传输最小进程控制信息。

## rtcp包结构

rtcp也是通过udp来发送的。内容很少。所以可以把多个rtcp包，封装在一个udp包里。

我的这个示例里有。

https://github.com/teddyxiong53/c_code/blob/master/myrtspd/src/include/rtcp.h

```
struct rtcp_header {
    u32 count:5;
    u32 padding:1;
    u32 version:2;
    u32 pt:8;
    u32 length:16;
};
```

```
enum rtcp_pkt_type {//包类型。
    SR = 200,//Sender Report。
    RR = 201,//Receiver Report。
    SDES = 202,//Source DEScription。
    BYE = 203,//bye bye，离开声明。
    APP = 204,//app。特殊应用包。
};
```

# SDP协议

sdp完全是一种session描述格式，对应文档RFC2327 。

可以跟http、rtsp一起使用。

也是基于文本的协议。这样可以保证有很好的可扩展性。

在流媒体里，描述媒体信息。

使用utf-8编码。

格式是键值对。

这个是我的myrtspd返回的内容。

```
v=0
o=rtspd 3734150656 3734150656
c=IN IP4 192.168.190.137
s=RTSP Session
i=rtspd 1.0 Streaming Server
u=1.h264
t=0 0
m=video 0 RTP/AVP 96
a=rtpmap:96 H264/90000
a=fmtp:96 packetization-mode=1;profile-level-id=1EE042;sprop-parameter-sets=QuAe2gLASRA=,zjCkgA==
a=control:rtsp://192.168.190.137/1.h264/trackID=0
```





# 参考资料

1、RTP协议学习大总结从原理到代码

https://wenku.baidu.com/view/aaad3d136edb6f1aff001fa5.html?sxts=1525008415053

2、RTP/RTSP/RTCP有什么区别？

https://www.zhihu.com/question/20278635

3、一个RtspServer的设计与实现和RTSP2.0简介

https://www.cnblogs.com/haibindev/p/7918733.html

4、开源RTSP 流媒体服务器

https://blog.csdn.net/funkri/article/details/8447329

5、RTSP/RTP Streaming Server Hello World

https://www.medialan.de/usecase0001.html

6、RTCP协议详解

https://blog.csdn.net/bytxl/article/details/50400987

7、视频流传输协议RTP/RTCP/RTSP/HTTP的区别

https://www.cnblogs.com/balabalala/p/8044057.html

8、RTP协议全解析（H264码流和PS流）

https://blog.csdn.net/chen495810242/article/details/39207305

9、FU-A分包方式，以及从RTP包里面得到H.264数据和AAC数据的方法

https://blog.csdn.net/wudebao5220150/article/details/13815313

10、rtsp、rtp tcp和udp链接方式区别

https://blog.csdn.net/yuanbinquan/article/details/60574375

11、SDP协议解析

https://blog.csdn.net/machh/article/details/51873690