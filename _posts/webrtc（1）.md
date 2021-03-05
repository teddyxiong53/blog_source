---
title: webrtc（1）
date: 2019-01-08 14:59:25
tags:
	- 视频

---

--

# 简介

webrtc是web Real-Time Communication网络实时通信的缩写。

表示一种支持网页浏览器进行语音和视频对话的技术。

谷歌在2010年收购了一家公司得到的这个技术。

并且在2011年开源了出来，在业内得到的广泛的支持，成为下一代的视频通话的标准。

WebRTC实现了基于网页的语音对话或视频通话，目的是无插件实现web端的实时通信的能力。

## 发展历史

经历过Adobe Flash、Microsoft SilverLight的失败，也经历过Skype的辉煌，

Google最终把目标放在Html5。

WebRTC实时通信（Web Real-Time Communication）是一项开源技术，



**用来在Web浏览器中实现实时直接的多媒体通信功能，**

它能够建立两个或更多的人之间的端到端的**音频和视频流连接。**

这项只需要使用HTML 5和简单的Javascript API，

**开发者可以很轻松的创建RTC应用，只要浏览器支持，就可在不安装任何扩展和插件的前提下进行实时音频和视频聊天，**

它的原始动机当然希望用这个开源工程击败微软的Skype和苹果的Facetime。



十余年来，WebRTC终于获得了绝大多数浏览器厂商的支持，可谓是十年媳妇熬成婆。

但这只是一种技术。

在实际的技术实践中，就算你有许多理论、有多牛的技术，但不管你如何努力，

都不能够直接的被表达为一种结果。

这种需要通过一种介质才能够间接的表达我们核心能力的神秘现象，那就是＂场景＂。



当然，场景的讨论很难，因为，只要是黑科技，一定是一种场景的表达而不是技术表达。

比如华为的鸿蒙操作系统，它可以通过一套OS来完成物联网全连接，但这不是场景。

它必须通过PC、Pad、手机、电视、汽车等等多种连接场景，

让你们感受到它的那种震憾，这就是场景所带给我们的体验和商业价值。



WebRTC何尝不是，十年时间，WebRTC孜孜不倦的在寻找场景。

各种 App 包括 WhatsApp、Facebook Manager、appear.in 和 TokBox 平台上。

甚至在 iOS 浏览器上的WebRTC实验和微软在 Edge 中增加了 MediaCapture 和 Stream API。

这是一种试图在商业应用中证明自己的能力的努力。

非常遗憾的是，十年时间，真正掌握企业通信的主流厂商一直沉默中，他们或许在等待企业级应用的节点的到来。

**因此，WebRTC的应用，一直处于边缘和非企业级商业应用的状态**



## 组成

视频引擎（VideoEngine）
音效引擎（VoiceEngine）
会议管理（Session Management）
iSAC：音效压缩
VP8：Google自家的WebM项目的视频编解码器
APIs（Native C++ API, Web API）

## api分类

WebRTC原生APIs文件是基于WebRTC规格书撰写而成，

这些API可分成

Network Stream API、 

RTCPeerConnection、

Peer-to-peer Data API

三类。





## 流程

WebRTC易于使用，只需极少步骤便可建立媒体会话。有些消息在浏览器和服务器之间流动，有些则直接在两个浏览器（成为对等端）之间流动。

最简单的场景就是这个webrtc三角形。

![1597053074038](../images/random_name/1597053074038.png)



具体步骤有11个步骤。

![1597053132977](../images/random_name/1597053132977.png)

```
1、浏览器M向web服务器请求网页。
2、web服务器向浏览器M返回带有webrtc js的网页。
3、浏览器L请求网页。
4、web服务器向浏览器L返回带有webrtc js的网页。
5、M决定跟L通信，所以通过js代码把自己的session对象（offer、提议）发送到web服务器。
6、web服务器把M的session对象发送到L的js。
7、L上的js将L的session对象（answer、应答）发送到web服务器。
8、web服务器转发应答到M的js。
9、M和L开始交互，确定访问对方的最佳方式。
10、M和L开始协商通信秘钥。
11、M和L交换语音和视频数据。
```

### WebRTC组成

![zucheng.webp.jpg](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/bVbzbZR)

- getUserMedia负责获取用户本地的多媒体数据
- RTCPeerConnection负责建立P2P连接以及传输多媒体数据。
- RTCDataChannel提供的一个信令通道实现双向通信

# 代码编译

官方没有把代码放在github。

下面这个是个人上传的。

https://github.com/JumpingYang001/webrtc

webrtc 全部下载到本地的话，大约会占用 6.4 G 的磁盘空间；

# 演示代码

https://github.com/webrtc/samples





# coturn

https://github.com/coturn/coturn

coturn是一个开源的turn和stun服务器代码。

一般大家把这个叫打洞服务器。



webrtc在连接之前，需要进行2个协商：

1、媒体协商。用sdp协议。

2、网络协商。这个叫candidate。

媒体协商是通话双方，例如A和B。A支持VP8和H264，B支持VP9和H264，那么协商的结果就是使用H264编码。

而对于网络协商

**彼此要了解对方的网络情况，这样才有可能找到一条相互通讯的链路**

**先说结论：(1)获取外网IP地址映射；（2）通过信令服务器（signal server）交换"网络信息"**

理想的网络情况是每个浏览器的电脑都是私有公网IP，可以直接进行点对点连接。

实际情况是：我们的电脑和电脑之前或大或小都是在某个局域网中，**需要NAT（Network Address Translation，网络地址转换）**

在解决WebRTC使用过程中的上述问题的时候，我们需要用到**STUN和TURN**。

**STUN**
STUN（Session Traversal Utilities for NAT，NAT会话穿越应用程序）是一种网络协议，

它允许位于NAT（或多重NAT）后的客户端找出自己的公网地址，

查出自己位于哪种类型的NAT之后，以及NAT为某一个本地端口所绑定的Internet端端口。

这些信息被用来在两个同时处于NAT路由器之后的主机之间**创建UDP通信**。

该协议由RFC 5389定义。

使用一句话说明STUN做的事情就是：告诉我你的公网IP地址+端口是什么。搭建STUN服务器很简单，媒体流传输是按照P2P的方式。

那么问题来了，**STUN并不是每次都能成功的为需要NAT的通话设备分配IP地址的，**

**P2P在传输媒体流时，使用的本地带宽，在多人视频通话的过程中，通话质量的好坏往往需要根据使用者本地的带宽确定。**

那么怎么办？TURN可以很好的解决这个问题。

**TURN**

TURN的全称为Traversal Using Relays around NAT，

是STUN/RFC5389的一个拓展，

主要添加了Relay功能。

如果终端在NAT之后， 那么在特定的情景下，有可能使得终端无法和其对等端（peer）进行直接的通信，

这时就需要公网的服务器作为一个中继， 对来往的数据进行转发。这个转发的协议就被定义为TURN。

在STUN分配公网IP失败后，可以通过TURN服务器请求公网IP地址作为中继地址。

这种方式的带宽由服务器端承担，在多人视频聊天的时候，本地带宽压力较小，

并且，根据Google的说明，TURN协议可以使用在所有的环境中。（单向数据200kbps 一对一通话）

从上面1/2点我们知道了2个客户端协商媒体信息和网络信息，那怎么去交换？

是不是需要一个中间商去做交换？

所以我们需要一个信令服务器（Signal server）转发彼此的媒体信息和网络信息。

**信令服务器不只是交互 媒体信息sdp和网络信息candidate，比如：**

**（1）房间管理**

**（2）人员进出房间**

## 建立连接的流程

![peer2peertimeline.png](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/bVbzbZS)

## 在云服务器上搭建

为了简单处理，使用docker方式来搭建。

这样安装卸载都比较方便。

https://github.com/ging/licode

# 简单示例

浏览器里的这个js api，就可以使用webrtc了。很简单。

只要实现一个函数就好了。

```
navigator.mediaDevices.getUserMedia(constraints)
.then(function(stream) {
  /* 使用这个stream stream */
})
.catch(function(err) {
  /* 处理error */
});
```

# Janus-gateway

这个是一个基于webrtc的流媒体服务器。

janus是Meetecho开发的一个WebRTC网关，

janus的主要作用就是它可以和你的内网设备和浏览器同时建立连接，

并将浏览器发来的音视频数据包如rtp/rtcp包，

通过自定义插件转发给你的内网设备，

也可以将你发给janus的音视频数据包，加密后转发给浏览器。

这样就完成了内网音视频服务器和外网浏览器的互通。



janus为我们完成了与浏览器建立会话的复杂逻辑，

并且提供给我们简单的插件机制来处理音视频数据。



对于PeerConnection连接的建立过程，

涉及到复杂的NAT穿透的ICE协议的实现，SDP的交换，DTLS-SRTP的握手和数据包加密发送，数据包接收后解密的复杂逻辑。

janus将我们从与浏览器交互的PeerConnection建立的过程中解脱出来，更专注于音视频业务逻辑。



## janus的设计思想 

janus基于插件思想，通过实现基础架构，完成了与浏览器链接的建立过程。

janus的插件主要完成一些必须的函数实现，如RTP/RTCP数据的接收。

我们通过实现自己的插件，来完成在将浏览器RTP数据转发到内网服务器的业务逻辑。

## janus的用途 

janus一般用于拓展已有视频会议系统，提供对浏览器客户端的支持。



安装

```
docker pull canyan/janus-gateway:latest
```

运行

```
docker run -itd  --name janus --hostname janus --network host canyan/janus-gateway:latest
```

这样可以跑起来。







# 参考资料

1、搭建WebRtc环境

https://www.cnblogs.com/wunaozai/p/5520084.html

2、webrtc

https://baike.baidu.com/item/WebRTC/5522744?fr=aladdin

3、WebRTC介绍及简单应用

https://www.cnblogs.com/vipzhou/p/7994927.html

4、2020：WebRTC应用之路

http://www.ccmw.net/article/170033.html

5、120行代码实现 浏览器WebRTC视频聊天

https://wdd.js.org/webrtc-tutorial-simple-video-chat.html

6、WebRTC入门与提高1：WebRTC基础入门

这个系列文章可以。

https://zhuanlan.zhihu.com/p/93107411

7、

https://zhuanlan.zhihu.com/p/93122564

8、WebRTC实现p2p视频通话

https://segmentfault.com/a/1190000020741658

9、WebRTC服务器——Licode 环境搭建

https://www.cnblogs.com/harlanc/p/10226614.html