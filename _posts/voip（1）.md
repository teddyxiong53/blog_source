---
title: voip（1）
date: 2020-02-19 17:43:51
tags:
	- 音频

---

--

# 资源收集

## 网站

https://www.voip-info.org 

这个网站号称是所有voip相关的内容都可以在这个上面找到。

https://en.wikipedia.org/wiki/Comparison_of_VoIP_software

对比各种不同的voip软件，比较齐全。



## 书籍

http://www.haifux.org/lectures/229/voipToHaifux.pdf



## 开源代码





WebRTC很有发展前景，它首先是开源项目。WebRTC在实时音视频传输的时候，特别是对于网络NAT技术，网络穿越技术解决方案上都有很独到的地方。WebRTC对于音视频本身的编解码，音频的前处理都有一些相关的方案，WebRTC在很多场景都是很不错的解决方案。

两个场景不一样，直播的时候可能会跳动，或者VOD播放的时候如果延时比较大也没有关系，延时超过200毫秒，500毫秒，甚至1秒都没事，直播虽然晚一秒也不妨碍观看和体验。

但是实时语音通信就不可以，超过300毫秒，甚至打电话1秒之后才回过来这肯定不行。

我不觉得它们会用RTC技术，它们还是会用RTMP推流，或者HLS切包发送这样的技术，

因为虽然会带来延时，但是在网络抖动处理，包括其他很多方面都能处理得更好。

所以适用的场景不一样，未来做不同技术的考虑点也会不一样。



Linux voip方案

通过[Ubuntu](https://so.csdn.net/so/search?q=Ubuntu&spm=1001.2101.3001.7020) 12.04 x64 部署opensips、rtpproxy、mediaproxy，

实现了sip服务、媒体转发等服务。

通过配置与测试，还支持ICE方式建立点对点的音视频会话。

花了些时间折腾，大家如有问题请留言沟通。

# 什么是voip

voip就是网络电话服务。

# voip怎么工作的

# 为什么使用voip

1、费用更低。

2、功能更丰富。

# sip协议是什么

全称是Session Initiation Protocol。

用来发送和处理通话session。

这个协议有时候被作为voip实现的事实标准。

是一个IETF标准。

跟它同一个生态位上的东西还有：IAX2。

SIP使用RTP协议做数据传输。

RTP使用tcp或udp来传输，可以用tls来加密。

PJSIP是SIP的一个代码实现。

# 树莓派搭建voip

https://ost.51cto.com/posts/21

# Asterisk

 Asterisk是一个全软件方式的PBX系统。

它可以运行在Linux，BSD，Windows(仿真的)以及 OS X上，

它提供了您希望从PBX那里获得的所有功能，而且还比PBX更多。

Asterisk支持4类VoIP的协议；

通过使用相对便宜的硬件，它可以与几乎全部基于标准的电话设备进行互联操作。



## 安装到树莓派

可以从[Raspberry Pi Asterisk](http://www.raspberry-asterisk.org/)官网下载最新版本的RasPBX。所有版本的RasPBX都是基于官方发布的Raspberry Pi OS。

现在您可以使用FreePBX Web界面来配置Asterisk，

添加您的VOIP提供商，

并为您的内部VOIP网络添加扩展。

大多数 VOIP 提供商都会为你提供使用 FreePBX 网页界面连接到其服务的步骤。

你还需要将每个VOIP电话指向Raspberry Pi的IP地址，这样它们就可以连接到Asterisk服务器。



参考资料

https://www.labno3.com/2021/07/13/installing-asterisk-on-the-raspberry-pi/

# PBX系统

PBX是用户电话交换机的缩写，是一个在企业内部使用的私有电话网络。

PBX电话系统的用户们须共用一定数量的外线，才能向外界拨打电话。

Private Branch Exchange，用户级交换机，即公司内部使用的电话业务网络，*系统*内部分机用户分享一定数量的外线。

传统的PBX利用电路交换的原理来实现集团电话的功能，而IP PBX则使用[TCP/IP协议](https://baike.baidu.com/item/TCP%2FIP协议/212915?fromModule=lemma_inlink)，利用包交换的原理，在[以太网](https://baike.baidu.com/item/以太网?fromModule=lemma_inlink)上实现了相同的功能。

传统PBX(专用[集团电话交换机](https://baike.baidu.com/item/集团电话交换机?fromModule=lemma_inlink))的缺点可以罗列很多：

专用、价格昂贵、不能简单实现CTI或VOIP、不能解决2000年问题等等。

IP PBX的出现可以解决这些问题：由于它构建于开放的编码，因此能够降低过高的设备、维护和升级等费用。

每一个重量级计算机和通信厂商都在IP PBX领域插上一脚。





参考资料

1、

https://www.3cx.com/global/cn/voip-sip-webrtc/pbx-phone-system/

2、

https://baike.baidu.com/item/PBX/3737223

# FreePBX



# PJSIP/PJSUA2

pjsip是一个开源的多媒体通话库，用C语言编写。项目开始于2005年。

支持协议：SIP、SDP、RTP、STUN、TURN、ICE。

把SIP协议跟多媒体框架和NAT组合起来。提供更加易用的high level接口。

最新的一个版本是2021年4月的2.11版本。

官网：

http://www.pjsip.org



https://www.hackster.io/leograba/setting-a-voip-sip-user-agent-with-embedded-linux-827a70#

# 参考资料

1、腾讯会议突围背后：端到端实时语音技术是如何保障交流通畅的？

https://www.e-learn.cn/topic/3528085	

2、What is VOIP?

https://www.voip-info.org/what-is-voip/