---
title: coap（一）
date: 2018-02-08 21:27:37
tags:
	- coap

---

# 1. 什么是coap 

因为http协议比较大，在资源有限的物联网设备上，跑http比较吃力。所以提出了一些精简的应用层协议。mqtt和coap是其中比较出名的。另外还有xmpp协议。

RFC文档在这。https://tools.ietf.org/html/rfc7252

coap是Constrained Application Protocol的缩写。字面含义是受限的应用协议。

coap协议的底层的udp协议。



使用请求/响应的交互模型。

用于机器与机器的通信。



coap协议的特点：

1、基于restful架构。

2、基于udp lite，允许ip多播。

3、定义了重传机制。保证可靠性。

4、提供了资源发现机制。

5、小巧。最小的包只有4个字节。

6、可以使用DTLS作为安全加密层。

7、资源消耗低。ram和rom消耗都低于10K。

8、支持观察模式，就是client不需要一直去查询server的数据。server会在自己数据变化时，主动下发给client。

9、支持块传输。就是有时候不得不发送较大的数据的时候用的。



一个通信的例子。

coap client通过get方法从server得到温度。

uri为：coap://www.xxx.com/temp



参考资料

1、MQTT和CoAP协议比较

https://blog.csdn.net/aa1215018028/article/details/82460597