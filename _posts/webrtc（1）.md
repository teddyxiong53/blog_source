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



webrtc 全部下载到本地的话，大约会占用 6.4 G 的磁盘空间；



经历过Adobe Flash、Microsoft SilverLight的失败，也经历过Skype的辉煌，Google最终把目标放在Html5。WebRTC实时通信（Web Real-Time Communication）是一项开源技术，

**用来在Web浏览器中实现实时直接的多媒体通信功能，**

它能够建立两个或更多的人之间的端到端的**音频和视频流连接。**

这项只需要使用HTML 5和简单的Javascript API，

开发者可以很轻松的创建RTC应用，只要浏览器支持，就可在不安装任何扩展和插件的前提下进行实时音频和视频聊天，

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



## 在哪里使用WebRTC?

- Chrome
- FireFox
- Opera
- Android
- iOS



参考资料

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