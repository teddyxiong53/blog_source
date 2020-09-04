---
title: webrtc（1）
date: 2019-01-08 14:59:25
tags:
	- 视频

---

1

webrtc是web Real-Time Communication网络实时通信的缩写。表示一种支持网页浏览器进行语音和视频对话的技术。

谷歌在2010年收购了一家公司得到的这个技术。并且在2011年开源了出来，在业内得到的广泛的支持，成为下一代的视频通话的标准。

视频引擎（VideoEngine）
音效引擎（VoiceEngine）
会议管理（Session Management）
iSAC：音效压缩
VP8：Google自家的WebM项目的视频编解码器
APIs（Native C++ API, Web API）

WebRTC原生APIs文件是基于WebRTC规格书撰写而成，

这些API可分成

Network Stream API、 

RTCPeerConnection、

Peer-to-peer Data API

三类。

WebRTC实现了基于网页的语音对话或视频通话，目的是无插件实现web端的实时通信的能力。



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



webrtc中的媒体

webrtc的代码：

https://github.com/JumpingYang001/webrtc

编译：



参考资料

1、搭建WebRtc环境

https://www.cnblogs.com/wunaozai/p/5520084.html

2、webrtc

https://baike.baidu.com/item/WebRTC/5522744?fr=aladdin

3、WebRTC介绍及简单应用

https://www.cnblogs.com/vipzhou/p/7994927.html